# Responsable de la interfaz de usuario del juego
# Maneja la inicializacion de Pygame, la creacion de la ventana
# y la integracion de los distintos componentes de la UI

import pygame
import sys
from core.backgammon import Backgammon
from core.constants import BLANCAS, NEGRAS, BOARD_POINTS, HOME_RANGE
from core.excepciones import (
	BackgammonError,
)
from pygame_ui.board_view import BoardView
from pygame_ui.constants import COLOR_BTN_RESTART, COLOR_BTN_EXIT, PLACEHOLDER_WHITE, PLACEHOLDER_BLACK
from pygame_ui.events_handler import EventsHandler


class GameUI:
	"""Orquestador simple: crea el juego y dibuja con BoardView.

	Mantiene la UI minimalista para mostrar el tablero y nombres con el layout clásico.
	"""

	def __init__(self, player1_name: str, player2_name: str, width=900, height=600):
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Backgammon - Pygame")
		self.clock = pygame.time.Clock()
		self.is_running = True

		# Núcleo del juego
		self.game = Backgammon(player1_name, BLANCAS, player2_name, NEGRAS)

		# Render del tablero con mismas medidas del diseño clásico
		self.board_view = BoardView(width, height)

		# Estado UI
		self.player1_name = player1_name
		self.player2_name = player2_name
		turno = self.game.turno_actual.obtener_color()
		nombre = self.game.turno_actual.obtener_nombre()
		self.message = f"Turno de {nombre} ({turno}). Espacio: tirar dados | Izq: seleccionar | Der: mover"
		self.dados_disponibles = []  # copia editable del turno actual
		self.seleccion = None  # None | int(0..23) | 'barra'
		self.destinos_resaltados = []  # lista de puntos o 'off'
		self._destino_a_dado = {}  # map destino -> valor de dado a consumir
		# Selección automática inicial si hay fichas en barra
		self._auto_select_bar()
		# Estado fin de juego
		self._game_over = False
		self._game_over_info = None  # dict con nombres, colores y borne-off
		# Manejador de eventos
		self.events = EventsHandler(self)

	def _color_actual(self):
		return self.game.turno_actual.obtener_color()

	def _direccion(self):
		# Blancas avanzan hacia índices altos, Negras hacia bajos
		return 1 if self._color_actual() == BLANCAS else -1

	def _top_checker_color(self, punto):
		board = self.game.estado_tablero()
		if 0 <= punto < BOARD_POINTS and board[punto]:
			return board[punto][-1]
		return None

	def _puede_mover_desde(self, punto):
		c = self._color_actual()
		return self._top_checker_color(punto) == c

	def _calcular_destinos_barra(self):
		"""Calcula entradas posibles desde la barra, devolviendo (destinos, mapa_dado)."""
		color = self._color_actual()
		board = self.game.tablero.mostrar_tablero()
		posibles = []
		m = {}
		for d in self.dados_disponibles:
			if color == BLANCAS:
				dest = d - 1
			else:
				dest = BOARD_POINTS - d
			if 0 <= dest < BOARD_POINTS:
				pila = board[dest]
				if (not pila) or (pila[-1] == color) or (len(pila) == 1):
					if dest not in posibles:
						posibles.append(dest)
					m[dest] = d
		return posibles, m

	def _calcular_destinos_mov(self, origen):
		"""Calcula destinos para mover desde 'origen', considerando dados y reglas básicas.

		Devuelve (destinos, mapa_dado). Puede incluir 'off' si se permite sacar.
		"""
		color = self._color_actual()
		dir_ = self._direccion()
		board = self.game.tablero.mostrar_tablero()
		posibles = []
		m = {}
		for d in self.dados_disponibles:
			dest = origen + dir_ * d
			if 0 <= dest < BOARD_POINTS:
				# Validación de bloqueo mediante API del tablero
				try:
					self.game.tablero.validar_movimiento(origen, dest, color)
					añadir = True
				except BackgammonError:
					añadir = False
				if añadir:
					if dest not in posibles:
						posibles.append(dest)
					m[dest] = d
			else:
				# Posible borne-off si está en home
				try:
					if self.game.todas_en_home():
						dist_off = (24 - origen) if color == BLANCAS else (origen + 1)
						# Nueva regla: si el dado es MAYOR O IGUAL a la distancia, puede sacar.
						if d >= dist_off:
							if 'off' not in posibles:
								posibles.append('off')
							m['off'] = d
				except BackgammonError:
					pass
		return posibles, m

	def _no_hay_mas_lejos_en_home(self, origen: int) -> bool:
		"""Devuelve True si no hay fichas propias más lejos del borne-off que 'origen' dentro del home.

		Para Blancas (18..23): 'más lejos' significa puntos mayores que 'origen'.
		Para Negras (0..5): 'más lejos' significa puntos menores que 'origen'.
		"""
		color = self._color_actual()
		board = self.game.tablero.mostrar_tablero()
		home = HOME_RANGE[color]
		if color == BLANCAS:
			candidatos = [p for p in home if p > origen]
		else:
			candidatos = [p for p in home if p < origen]
		for p in candidatos:
			if board[p] and board[p][-1] == color:
				return False
		return True

	def _recalcular_resaltados(self):
		self.destinos_resaltados = []
		self._destino_a_dado = {}
		color = self._color_actual()
		# Si hay fichas en barra, sólo se puede reingresar
		if self.game.fichas_en_barra(color) > 0:
			dest, mm = self._calcular_destinos_barra()
			self.destinos_resaltados = dest
			self._destino_a_dado = mm
			return
		# Si hay origen seleccionado
		if isinstance(self.seleccion, int):
			dest, mm = self._calcular_destinos_mov(self.seleccion)
			self.destinos_resaltados = dest
			self._destino_a_dado = mm

	def _hay_movimientos_disponibles(self):
		"""Chequea si hay algún movimiento posible con los dados actuales."""
		if not self.dados_disponibles:
			return False
		color = self._color_actual()
		# Reingreso prioritario
		if self.game.fichas_en_barra(color) > 0:
			dest, _ = self._calcular_destinos_barra()
			return len(dest) > 0
		# Revisar cada punto del tablero del jugador
		board = self.game.tablero.mostrar_tablero()
		for i in range(BOARD_POINTS):
			if board[i] and board[i][-1] == color:
				dest, _ = self._calcular_destinos_mov(i)
				if dest:
					return True
		return False

	def _handle_events(self):
		self.events.handle_events()

	def handle_space(self):
		# Tirar dados si no hay aún
		if not self.dados_disponibles and not self._game_over:
			try:
				vals = self.game.tirar_dados()
				self.dados_disponibles = list(vals)
				# Selección automática de barra si aplica
				if self.game.fichas_en_barra(self._color_actual()) > 0:
					self.seleccion = 'barra'
					self._recalcular_resaltados()
					self.message = "Tiene fichas en barra. Seleccione destino de reingreso"
				else:
					self.seleccion = None
					self._recalcular_resaltados()
					turno = self.game.turno_actual.obtener_color()
					nombre = self.game.turno_actual.obtener_nombre()
					self.message = f"Turno de {nombre} ({turno}). Dados: {self.dados_disponibles}. Seleccione origen."
			except BackgammonError as e:
				self.message = e.message or str(e)

	def exit_game(self):
		self.is_running = False
		pygame.quit()
		sys.exit()

	def left_click(self, pos):
		if self.game.juego_terminado():
			ganador = self.game.obtener_ganador() or ""
			self.message = f"Juego terminado. Ganó {ganador}."
			return
		p = self.board_view.get_point_from_mouse(pos)
		if p is None:
			return
		color = self._color_actual()
		# Si hay fichas en barra, forzar reingreso cuando sí hay dados.
		if self.game.fichas_en_barra(color) > 0 and self.dados_disponibles:
			if p == 'barra':
				self.seleccion = 'barra'
				self._recalcular_resaltados()
				self.message = "Seleccione destino de reingreso (click derecho para mover)"
				return
			# Si ya seleccionó barra y hace click en un destino válido con izquierdo, no mover
			if self.seleccion == 'barra' and isinstance(p, int) and p in self.destinos_resaltados:
				self.message = "Use click derecho para reingresar"
			return
		# Intentar aplicar movimiento o borne-off (prioridad) si hay una selección previa
		if isinstance(self.seleccion, int):
			# Con click izquierdo no se mueve; permitir cambiar selección a otra ficha propia
			if isinstance(p, int) and self._puede_mover_desde(p):
				self.seleccion = p
				if self.dados_disponibles:
					self._recalcular_resaltados()
					if not self.destinos_resaltados:
						self.message = "Sin destinos para esa ficha. Puede elegir otra."
					else:
						self.message = "Seleccione destino (click derecho para mover)"
				else:
					self.message = "Tire los dados (ESPACIO)."
				return
			# Si hace click en un destino válido con izquierdo, recordar que debe usar derecho
			if (p == 'off' and 'off' in self.destinos_resaltados) or (isinstance(p, int) and p in self.destinos_resaltados):
				self.message = "Use click derecho para mover"
				return
		# Movimiento normal: seleccionar/deseleccionar fichas propias (si no se movió arriba)
		if isinstance(p, int) and self._puede_mover_desde(p):
			# Toggle si ya estaba seleccionado; si era otro, cambiar selección
			if self.seleccion == p:
				self.seleccion = None
				self.destinos_resaltados = []
				self._destino_a_dado = {}
				if not self.dados_disponibles:
					self.message = "Tire los dados (ESPACIO)."
				else:
					turno = self.game.turno_actual.obtener_color()
					nombre = self.game.turno_actual.obtener_nombre()
					self.message = f"Turno de {nombre} ({turno}). Dados: {self.dados_disponibles}. Seleccione origen."
			else:
				self.seleccion = p
				# Sólo recalcular destinos si hay dados; sin dados no hay resaltados
				if self.dados_disponibles:
					self._recalcular_resaltados()
					if not self.destinos_resaltados:
						self.message = "Sin destinos para esa ficha. Puede elegir otra."
					else:
						self.message = "Seleccione destino (click derecho para mover)"
				else:
					self.message = "Tire los dados (ESPACIO)."
			return
		# Si clickea el mismo seleccionado y no es jugable, deseleccionar
		if self.seleccion == p:
			self.seleccion = None
			self.destinos_resaltados = []
			self._destino_a_dado = {}
			return

	def right_click(self, pos):
		"""Click derecho: intentar mover desde la selección actual al destino clickeado."""
		if self.game.juego_terminado():
			return
		p = self.board_view.get_point_from_mouse(pos)
		if p is None:
			return
		color = self._color_actual()
		# Reingreso desde barra con click derecho al destino
		if self.game.fichas_en_barra(color) > 0 and self.dados_disponibles:
			if self.seleccion != 'barra':
				# Ayuda: si no está seleccionada la barra, indicar cómo
				self.message = "Seleccione 'barra' con click izquierdo para reingresar"
				return
			if isinstance(p, int) and p in self.destinos_resaltados:
				dado = self._destino_a_dado.get(p)
				try:
					self.game.reingresar_desde_barra(p)
					self._consumir_dado(dado)
					if self.game.fichas_en_barra(color) > 0 and self.dados_disponibles:
						self.seleccion = 'barra'
						self._recalcular_resaltados()
						self.message = "Seleccione destino de reingreso (click derecho para mover)"
					else:
						self.seleccion = None
						self._post_move_update()
				except BackgammonError as e:
					self.message = e.message or str(e)
			return
		# Movimiento normal o borne-off con selección activa
		if isinstance(self.seleccion, int):
			if p == 'off' and 'off' in self.destinos_resaltados:
				dado = self._destino_a_dado.get('off')
				try:
					self.game.sacar_ficha_fuera(self.seleccion)
					self._consumir_dado(dado)
					self.seleccion = None
					self._post_move_update()
				except BackgammonError as e:
					self.message = e.message or str(e)
			elif isinstance(p, int) and p in self.destinos_resaltados:
				dado = self._destino_a_dado.get(p)
				try:
					self.game.mover(self.seleccion, p)
					self._consumir_dado(dado)
					self.seleccion = None
					self._post_move_update()
				except BackgammonError as e:
					self.message = e.message or str(e)
			return
		# Si no hay selección, no seleccionar con derecho
		if isinstance(p, int) and self._puede_mover_desde(p):
			self.message = "Use click izquierdo para seleccionar origen"

	def _consumir_dado(self, valor):
		# Eliminar una ocurrencia del valor en dados_disponibles
		try:
			idx = self.dados_disponibles.index(valor)
			self.dados_disponibles.pop(idx)
		except ValueError:
			pass

	def _post_move_update(self):
		# Tras un movimiento, verificar fin de juego, recalcular posibles y mensaje
		if self.game.juego_terminado():
			ganador = self.game.obtener_ganador() or ""
			self.message = f"¡{ganador} ganó!"
			self._game_over = True
			# Construir info de marcador: fichas borne-off por color
			try:
				j1 = self.game.jugador1
				j2 = self.game.jugador2
				from core.constants import INITIAL_CHECKERS
				w = j1 if j1.obtener_nombre() == ganador else j2
				l = j2 if w is j1 else j1
				w_off = INITIAL_CHECKERS - int(w.mostrar_fichas_restantes())
				l_off = INITIAL_CHECKERS - int(l.mostrar_fichas_restantes())
				self._game_over_info = {
					"winner_name": w.obtener_nombre(),
					"winner_color": w.obtener_color(),
					"winner_off": w_off,
					"loser_name": l.obtener_nombre(),
					"loser_color": l.obtener_color(),
					"loser_off": l_off,
				}
			except Exception:
				self._game_over_info = None
			self.destinos_resaltados = []
			return
		# Recalcular
		self._recalcular_resaltados()
		# Si no hay dados o no hay movimientos posibles -> pasar de turno automáticamente
		if not self.dados_disponibles or not self._hay_movimientos_disponibles():
			try:
				self.game.cambiar_turno()
				self.dados_disponibles = []
				self.seleccion = None
				self.destinos_resaltados = []
				self._destino_a_dado = {}
				turno = self.game.turno_actual.obtener_color()
				nombre = self.game.turno_actual.obtener_nombre()
				self.message = f"Turno de {nombre} ({turno}). Espacio para tirar dados."
				# Selección automática de barra si aplica
				self._auto_select_bar()
			except BackgammonError as e:
				self.message = e.message or str(e)
		else:
			turno = self.game.turno_actual.obtener_color()
			nombre = self.game.turno_actual.obtener_nombre()
			self.message = f"Turno de {nombre} ({turno}). Dados: {self.dados_disponibles}. Seleccione origen."

	def _auto_select_bar(self):
		"""Si el jugador actual tiene fichas en barra, selecciona 'barra' automáticamente."""
		try:
			if self.game.fichas_en_barra(self._color_actual()) > 0:
				self.seleccion = 'barra'
				self._recalcular_resaltados()
		except BackgammonError:
			pass

	def _render(self):
		# Tablero y fichas
		self.board_view.draw_board(self.screen)
		self.board_view.draw_checkers(self.screen, self.game)
		self.board_view.draw_names(
			self.screen,
			self.player1_name,
			self.player2_name,
			active_color=self.game.turno_actual.obtener_color(),
		)
		# Dados y resaltados
		self.board_view.draw_dados(self.screen, self.dados_disponibles)
		self.board_view.draw_highlights(self.screen, self.destinos_resaltados, self.seleccion)
		self.board_view.draw_message_bar(self.screen, self.message)
		# Overlay de fin de juego
		if self._game_over:
			self._draw_game_over_overlay()
		pygame.display.flip()

	def handle_game_over_click(self, pos):
		if not self._game_over:
			return
		btns = getattr(self, "_overlay_buttons", None)
		if not btns:
			return
		if btns.get('restart') and btns['restart'].collidepoint(pos):
			self._restart_game()
		elif btns.get('exit') and btns['exit'].collidepoint(pos):
			self.exit_game()

	def _draw_game_over_overlay(self):
		# Fondo semitransparente
		overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 150))
		self.screen.blit(overlay, (0, 0))
		# Panel central
		w, h = self.screen.get_size()
		panel_w, panel_h = int(w * 0.7), int(h * 0.5)
		panel_rect = pygame.Rect((w - panel_w)//2, (h - panel_h)//2, panel_w, panel_h)
		pygame.draw.rect(self.screen, (245, 240, 220), panel_rect, border_radius=10)
		pygame.draw.rect(self.screen, (50, 50, 50), panel_rect, 3, border_radius=10)
		# Textos
		title_font = pygame.font.SysFont("arial", 32, bold=True)
		text_font = pygame.font.SysFont("arial", 24)
		title = title_font.render("¡Felicitaciones!", True, (0,0,0))
		self.screen.blit(title, (panel_rect.centerx - title.get_width()//2, panel_rect.top + 20))
		if self._game_over_info:
			wi = self._game_over_info
			line1 = text_font.render(f"Ganador: {wi['winner_name']} ({wi['winner_color']})", True, (0,0,0))
			line2 = text_font.render(f"Marcador: {wi['winner_name']} {wi['winner_off']} - {wi['loser_off']} {wi['loser_name']}", True, (0,0,0))
			self.screen.blit(line1, (panel_rect.centerx - line1.get_width()//2, panel_rect.top + 80))
			self.screen.blit(line2, (panel_rect.centerx - line2.get_width()//2, panel_rect.top + 120))
		else:
			info = text_font.render("Partida finalizada.", True, (0,0,0))
			self.screen.blit(info, (panel_rect.centerx - info.get_width()//2, panel_rect.centery))

		# Botones
		btn_w, btn_h = 140, 44
		gap = 30
		btn_restart = pygame.Rect(0, 0, btn_w, btn_h)
		btn_exit = pygame.Rect(0, 0, btn_w, btn_h)
		btn_restart.center = (panel_rect.centerx - (btn_w//2 + gap), panel_rect.bottom - 60)
		btn_exit.center = (panel_rect.centerx + (btn_w//2 + gap), panel_rect.bottom - 60)
		pygame.draw.rect(self.screen, COLOR_BTN_RESTART, btn_restart, border_radius=6)
		pygame.draw.rect(self.screen, COLOR_BTN_EXIT, btn_exit, border_radius=6)
		lbl_r = text_font.render("Reiniciar", True, (255,255,255))
		lbl_e = text_font.render("Finalizar", True, (255,255,255))
		self.screen.blit(lbl_r, (btn_restart.centerx - lbl_r.get_width()//2, btn_restart.centery - lbl_r.get_height()//2))
		self.screen.blit(lbl_e, (btn_exit.centerx - lbl_e.get_width()//2, btn_exit.centery - lbl_e.get_height()//2))
		self._overlay_buttons = { 'restart': btn_restart, 'exit': btn_exit }

	def _restart_game(self):
		"""Reinicia la partida manteniendo los mismos nombres y colores."""
		p1, p2 = self.player1_name, self.player2_name
		self.game = Backgammon(p1, BLANCAS, p2, NEGRAS)
		self.dados_disponibles = []
		self.seleccion = None
		self.destinos_resaltados = []
		self._destino_a_dado = {}
		self._game_over = False
		self._game_over_info = None
		self.message = f"Turno de {self.game.turno_actual.obtener_nombre()} ({self.game.turno_actual.obtener_color()}). Espacio: tirar dados | Izq: seleccionar | Der: mover"
		self._auto_select_bar()


	def run(self):
		while self.is_running:
			self._handle_events()
			self._render()
			self.clock.tick(60)

		pygame.quit()
		sys.exit()


def main():
	try:
		print("=== BACKGAMMON - PYGAME ===")
		# Validación: no permitir placeholders ni vacío
		while True:
			p1 = input("Nombre del Jugador 1 (Blancas): ").strip()
			if p1 and p1.lower() != PLACEHOLDER_WHITE.lower():
				break
			print("Nombre inválido. No se permite vacío ni 'Jugador 1'.")
		while True:
			p2 = input("Nombre del Jugador 2 (Negras): ").strip()
			if p2 and p2.lower() != PLACEHOLDER_BLACK.lower():
				break
			print("Nombre inválido. No se permite vacío ni 'Jugador 2'.")
		ui = GameUI(p1, p2)
		ui.run()
	except KeyboardInterrupt:
		print("\nJuego interrumpido por el usuario.")
	except Exception as e:
		print(f"Error ejecutando el juego: {e}")
		pygame.quit()
		sys.exit()


if __name__ == "__main__":
	main()