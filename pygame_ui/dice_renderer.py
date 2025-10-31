#FINALIZADO#
import pygame
from pygame_ui.constants import DICE_SIZE, DICE_GAP


class DiceRenderer:
	"""Renderiza los dados en la barra central, centrados verticalmente.

	Se apoya en la geometría de BoardView (márgenes, ancho de barra, etc.).
	"""

	def __init__(self, size: int = DICE_SIZE, gap: int = DICE_GAP):
		self.size = size
		self.gap = gap

	def draw_on_bar(self, view, screen, valores):
		"""Dibuja hasta 4 dados en la barra central.

		view: instancia de BoardView (usa sus propiedades de layout)
		screen: superficie pygame
		valores: lista de valores de dados
		"""
		if not valores:
			return

		tablero_top = view.margin
		tablero_bottom = view.height - view.message_bar_height - view.bottom_labels_band

		# Centro de la barra
		bar_left = view.margin + 6 * view.triangle_width
		bar_center_x = bar_left + view.center_bar_width / 2

		n = min(4, len(valores))
		total_h = n * self.size + (n - 1) * self.gap
		start_y = (tablero_top + view.top_labels_band) + (((tablero_bottom - (tablero_top + view.top_labels_band)) - total_h) / 2)

		def dibujar_dado(cx, cy, valor):
			rect = pygame.Rect(0, 0, self.size, self.size)
			rect.center = (cx, cy)
			pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=4)
			pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=4)

			# Pips
			r = 3
			ox, oy = rect.left + self.size * 0.25, rect.top + self.size * 0.25
			mx, my = rect.centerx, rect.centery
			px, py = rect.right - self.size * 0.25, rect.bottom - self.size * 0.25
			posiciones = {
				1: [(mx, my)],
				2: [(ox, oy), (px, py)],
				3: [(ox, oy), (mx, my), (px, py)],
				4: [(ox, oy), (px, oy), (ox, py), (px, py)],
				5: [(ox, oy), (px, oy), (mx, my), (ox, py), (px, py)],
				6: [(ox, oy), (px, oy), (ox, my), (px, my), (ox, py), (px, py)],
			}
			for (pxx, pyy) in posiciones.get(int(valor), []):
				pygame.draw.circle(screen, (0, 0, 0), (int(pxx), int(pyy)), r)

		# Disposición vertical centrada
		for idx, val in enumerate(valores[:4]):
			cx = bar_center_x
			cy = start_y + idx * (self.size + self.gap)
			dibujar_dado(cx, cy, val)

