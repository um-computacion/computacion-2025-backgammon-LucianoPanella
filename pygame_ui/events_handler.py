import pygame


class EventsHandler:
	"""Centraliza el manejo de eventos de Pygame y delega en GameUI."""

	def __init__(self, game_ui):
		self.ui = game_ui

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.ui.exit_game()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.ui.exit_game()
				elif event.key == pygame.K_SPACE:
					self.ui.handle_space()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Si hay overlay de fin de juego, priorizar botones
				if self.ui._game_over and event.button == 1:
					self.ui.handle_game_over_click(event.pos)
					continue
				if event.button == 1:
					self.ui.left_click(event.pos)
				elif event.button == 3:
					self.ui.right_click(event.pos)

