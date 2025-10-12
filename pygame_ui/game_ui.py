# Responsable de la interfaz de usuario del juego
# Maneja la inicializacion de Pygame, la creacion de la ventana
# y la integracion de los distintos componentes de la UI


import pygame
import sys
from core.backgammon import Backgammon
from .constants import *
from .board_renderer import BoardRenderer
from .dice_renderer import DiceRenderer
from .events_handler import EventsHandler

class GameUI:
    def __init__(self, player1_name="Jugador 1", player2_name="Jugador 2"):
        """
        Inicializa la interfaz gráfica del juego.
        
        Args:
            player1_name (str): Nombre del primer jugador
            player2_name (str): Nombre del segundo jugador
        """
        # Inicializar Pygame
        pygame.init()
        
        # Configurar pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon - Pygame")
        self.clock = pygame.time.Clock()
        
        # Inicializar juego
        self.game = Backgammon(player1_name, "Blancas", player2_name, "Negras")
        self.game.tablero.inicializar_piezas()
        
        # Inicializar componentes
        self.board_renderer = BoardRenderer(self.screen)
        self.dice_renderer = DiceRenderer(self.screen)
        self.events_handler = EventsHandler(self.game, self.board_renderer, self.dice_renderer)
        
        # Fuentes
        self.font_large = pygame.font.Font(None, FONT_SIZES['LARGE'])
        self.font_medium = pygame.font.Font(None, FONT_SIZES['MEDIUM'])
        self.font_small = pygame.font.Font(None, FONT_SIZES['SMALL'])
        
        # Estado de la interfaz
        self.running = True
        
    def run(self):
        """Loop principal del juego."""
        print("=== BACKGAMMON - PYGAME ===")
        print("Controles:")
        print("- Click: Seleccionar/mover fichas")
        print("- Espacio: Tirar dados")
        print("- Enter: Pasar turno")
        print("- Escape: Limpiar selección")
        print("- Ctrl+R: Reiniciar juego")
        print("==========================")
        
        while self.running:
            # Procesar eventos
            events = pygame.event.get()
            self.running = self.events_handler.handle_events(events)
            
            # Renderizar
            self._render()
            
            # Control de FPS
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def _render(self):
        """Renderiza todos los elementos en pantalla."""
        # Limpiar pantalla
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Renderizar tablero
        tablero_state = self.game.estado_tablero()
        self.board_renderer.draw_board(tablero_state)
        
        # Destacar posición seleccionada
        selected_pos = self.events_handler.get_selected_position()
        if selected_pos is not None:
            self._highlight_selected_position(selected_pos)
            
        # Renderizar dados
        dados_actuales = getattr(self.game, 'dados_actuales', [])
        self.dice_renderer.draw_dice(dados_actuales, (750, 100))
        
        # Renderizar botón de dados
        dice_enabled = not self.events_handler.is_dice_rolled()
        self.dice_renderer.draw_roll_button((750, 150), dice_enabled)
        
        # Renderizar información del juego
        self._render_game_info()
        
        # Renderizar estado del turno
        self._render_turn_info()
        
        # Verificar fin del juego
        if self.game.juego_terminado():
            self._render_game_over()
            
        # Actualizar pantalla
        pygame.display.flip()
        
    def _highlight_selected_position(self, position):
        """
        Destaca una posición seleccionada en el tablero.
        
        Args:
            position (int): Posición a destacar
        """
        # Calcular coordenadas de la posición
        if position < 12:
            visual_pos = 23 - position
            x = BOARD_MARGIN + (visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            if visual_pos >= 6:
                x += BAR_WIDTH
            y = BOARD_MARGIN + TRIANGLE_HEIGHT // 2
        else:
            visual_pos = position - 12
            x = BOARD_MARGIN + (5 - visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            if visual_pos < 6:
                x += BAR_WIDTH
            y = BOARD_MARGIN + TRIANGLE_HEIGHT + TRIANGLE_HEIGHT // 2
            
        # Dibujar círculo de selección
        pygame.draw.circle(self.screen, COLORS['SELECTED'], (int(x), int(y)), 30, 4)
        
    def _render_game_info(self):
        """Renderiza información general del juego."""
        y_offset = 250
        
        # Información de jugadores
        player1_info = self.game.estado_jugador(self.game.jugador1)
        player2_info = self.game.estado_jugador(self.game.jugador2)
        
        # Jugador 1
        text = self.font_medium.render(f"{player1_info['nombre']} ({player1_info['color']})", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset))
        
        text = self.font_small.render(f"Fichas restantes: {player1_info['fichas_restantes']}", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset + 25))
        
        text = self.font_small.render(f"En barra: {player1_info['en_barra']}", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset + 45))
        
        # Jugador 2
        y_offset += 80
        text = self.font_medium.render(f"{player2_info['nombre']} ({player2_info['color']})", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset))
        
        text = self.font_small.render(f"Fichas restantes: {player2_info['fichas_restantes']}", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset + 25))
        
        text = self.font_small.render(f"En barra: {player2_info['en_barra']}", True, COLORS['TEXT'])
        self.screen.blit(text, (750, y_offset + 45))
        
    def _render_turn_info(self):
        """Renderiza información del turno actual."""
        current_player = self.game.turno_actual.obtener_nombre()
        current_color = self.game.turno_actual.obtener_color()
        
        # Turno actual
        text = self.font_large.render("TURNO ACTUAL:", True, COLORS['TEXT'])
        self.screen.blit(text, (750, 450))
        
        color = COLORS['WHITE_PIECE'] if current_color == 'Blancas' else COLORS['BLACK_PIECE']
        text = self.font_medium.render(f"{current_player}", True, color)
        self.screen.blit(text, (750, 480))
        
        # Dados disponibles
        dados_disponibles = getattr(self.game, 'dados_actuales', [])
        if dados_disponibles:
            text = self.font_small.render(f"Dados disponibles: {dados_disponibles}", True, COLORS['TEXT'])
            self.screen.blit(text, (750, 510))
            
        # Instrucciones
        y = 550
        instructions = [
            "CONTROLES:",
            "Click: Seleccionar/Mover",
            "Espacio: Tirar dados",
            "Enter: Pasar turno",
            "Escape: Limpiar selección"
        ]
        
        for i, instruction in enumerate(instructions):
            color = COLORS['TEXT'] if i == 0 else COLORS['BOARD_LIGHT']
            font = self.font_small if i > 0 else self.font_medium
            text = font.render(instruction, True, color)
            self.screen.blit(text, (750, y + i * 20))
            
    def _render_game_over(self):
        """Renderiza pantalla de fin de juego."""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Mensaje de victoria
        ganador = self.game.obtener_ganador()
        text = self.font_large.render("¡JUEGO TERMINADO!", True, COLORS['TEXT'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        text = self.font_medium.render(f"¡{ganador} ha ganado!", True, COLORS['SELECTED'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        text = self.font_small.render("Presiona Ctrl+R para reiniciar", True, COLORS['TEXT'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(text, text_rect)

def main():
    """Función principal para ejecutar el juego."""
    try:
        # Solicitar nombres de jugadores
        print("=== BACKGAMMON - PYGAME ===")
        player1_name = input("Nombre del Jugador 1 (Blancas): ") or "Jugador 1"
        player2_name = input("Nombre del Jugador 2 (Negras): ") or "Jugador 2"
        
        # Iniciar juego
        game_ui = GameUI(player1_name, player2_name)
        game_ui.run()
        
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"Error ejecutando el juego: {e}")

if __name__ == "__main__":
    main()