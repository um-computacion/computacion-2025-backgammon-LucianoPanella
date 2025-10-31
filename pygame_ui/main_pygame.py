#FINALIZADO#
import pygame
from pygame_ui.game_ui import GameUI
from pygame_ui.constants import (
	SCREEN_WIDTH, SCREEN_HEIGHT,
	NAME_SCREEN_WIDTH, NAME_SCREEN_HEIGHT,
	PLACEHOLDER_WHITE, PLACEHOLDER_BLACK,
	COLOR_INPUT_ACTIVE, COLOR_INPUT_INACTIVE,
	COLOR_BG_NAME, COLOR_FIELD_BG,
	COLOR_BTN_RESTART as BTN_BG,
)


def ask_names_pygame():
	"""Pantalla simple en Pygame para ingresar nombres de Blancas y Negras."""
	WIDTH, HEIGHT = NAME_SCREEN_WIDTH, NAME_SCREEN_HEIGHT
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Backgammon - Ingresar nombres")
	clock = pygame.time.Clock()
	font_header = pygame.font.SysFont("arial", 36, bold=True)
	font_title = pygame.font.SysFont("arial", 28, bold=True)
	font = pygame.font.SysFont("arial", 22)

	# Campos - separacion levemente mayor para legibilidad
	input_rect_blancas = pygame.Rect(WIDTH//2 - 260, HEIGHT//2 - 50, 300, 40)
	input_rect_negras = pygame.Rect(WIDTH//2 - 260, HEIGHT//2 + 30, 300, 40)
	btn_rect = pygame.Rect(WIDTH//2 + 60, input_rect_negras.top + 50, 120, 40)

	color_active = COLOR_INPUT_ACTIVE
	color_inactive = COLOR_INPUT_INACTIVE
	bg = COLOR_BG_NAME
	field_bg = COLOR_FIELD_BG
	btn_bg = BTN_BG
	btn_text = (255, 255, 255)

	active_field = None  # 'blancas' | 'negras' | None
	nombre_blancas = PLACEHOLDER_WHITE
	nombre_negras = PLACEHOLDER_BLACK
	edited_blancas = False
	edited_negras = False

	# Validación: no permitir placeholders ni nombres vacíos
	error_msg = ""

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if input_rect_blancas.collidepoint(event.pos):
					active_field = 'blancas'
					if not edited_blancas and nombre_blancas == PLACEHOLDER_WHITE:
						nombre_blancas = ""
						edited_blancas = True
				elif input_rect_negras.collidepoint(event.pos):
					active_field = 'negras'
					if not edited_negras and nombre_negras == PLACEHOLDER_BLACK:
						nombre_negras = ""
						edited_negras = True
				elif btn_rect.collidepoint(event.pos):
					nb = (nombre_blancas or "").strip()
					nn = (nombre_negras or "").strip()
					if not nb or nb.lower() == PLACEHOLDER_WHITE.lower() or not nn or nn.lower() == PLACEHOLDER_BLACK.lower():
						error_msg = "Ingresá nombres reales: no se permiten 'Jugador 1' ni 'Jugador 2'."
					else:
						return nb, nn
				else:
					active_field = None
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					nb = (nombre_blancas or "").strip()
					nn = (nombre_negras or "").strip()
					if not nb or nb.lower() == PLACEHOLDER_WHITE.lower() or not nn or nn.lower() == PLACEHOLDER_BLACK.lower():
						error_msg = "Ingresá nombres reales: no se permiten 'Jugador 1' ni 'Jugador 2'."
					else:
						return nb, nn
				elif active_field is not None:
					if event.key == pygame.K_BACKSPACE:
						if active_field == 'blancas':
							nombre_blancas = nombre_blancas[:-1]
						else:
							nombre_negras = nombre_negras[:-1]
					else:
						char = event.unicode
						if char.isprintable():
							if active_field == 'blancas':
								# limpiar placeholder si aún no se editó
								if not edited_blancas and nombre_blancas == PLACEHOLDER_WHITE:
									nombre_blancas = ""
									edited_blancas = True
								nombre_blancas += char
							else:
								if not edited_negras and nombre_negras == PLACEHOLDER_BLACK:
									nombre_negras = ""
									edited_negras = True
								nombre_negras += char

		screen.fill(bg)
		# Encabezado y subtitulo
		header = font_header.render("Bienvenido a BACKGAMMON", True, (0,0,0))
		screen.blit(header, (WIDTH//2 - header.get_width()//2, 12))
		title = font_title.render("Ingresar nombres", True, (0,0,0))
		screen.blit(title, (WIDTH//2 - title.get_width()//2, 12 + header.get_height() + 8))

		# Labels
		lbl_b = font.render("Blancas:", True, (0,0,0))
		lbl_n = font.render("Negras:", True, (0,0,0))
		screen.blit(lbl_b, (input_rect_blancas.left, input_rect_blancas.top - 28))
		screen.blit(lbl_n, (input_rect_negras.left, input_rect_negras.top - 28))

		# Campos
		pygame.draw.rect(screen, field_bg, input_rect_blancas, border_radius=6)
		pygame.draw.rect(screen, field_bg, input_rect_negras, border_radius=6)
		pygame.draw.rect(screen, color_active if active_field=='blancas' else color_inactive, input_rect_blancas, 2, border_radius=6)
		pygame.draw.rect(screen, color_active if active_field=='negras' else color_inactive, input_rect_negras, 2, border_radius=6)

		text_b = font.render(nombre_blancas, True, (0,0,0))
		text_n = font.render(nombre_negras, True, (0,0,0))
		screen.blit(text_b, (input_rect_blancas.left + 8, input_rect_blancas.top + 8))
		screen.blit(text_n, (input_rect_negras.left + 8, input_rect_negras.top + 8))

		# Botón jugar
		pygame.draw.rect(screen, btn_bg, btn_rect, border_radius=6)
		btn_txt = font.render("Jugar", True, btn_text)
		screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width()//2, btn_rect.centery - btn_txt.get_height()//2))

		# Mensaje de error
		if error_msg:
			err = font.render(error_msg, True, (200, 30, 30))
			screen.blit(err, (WIDTH//2 - err.get_width()//2, btn_rect.bottom + 12))

		pygame.display.flip()
		clock.tick(60)


def main():
	pygame.init()
	try:
		# Pantalla de nombres
		nombre_blancas, nombre_negras = ask_names_pygame()
		# Lanzar el juego
		ui = GameUI(nombre_blancas, nombre_negras, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
		ui.run()
	finally:
		pygame.quit()


if __name__ == "__main__":
	main()

