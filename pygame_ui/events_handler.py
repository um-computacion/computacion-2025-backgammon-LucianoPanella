# Responsable de manejar los eventos de la interfaz de usuario
# como clics de botones, movimientos del mouse y entradas de teclado
# Se encarga de interactuar con la logica del juego (Core)
# y actualizar la interfaz de usuario en consecuencia


import pygame
from .constants import *

class EventsHandler:
    def __init__(self, game, board_renderer, dice_renderer):
        """
        Inicializa el manejador de eventos.
        
        Args:
            game: Instancia del juego Backgammon
            board_renderer: Renderizador del tablero
            dice_renderer: Renderizador de dados
        """
        self.game = game
        self.board_renderer = board_renderer
        self.dice_renderer = dice_renderer
        self.selected_position = None
        self.dice_rolled = False
        
    def handle_events(self, events):
        """
        Procesa todos los eventos de la cola.
        
        Args:
            events (list): Lista de eventos de pygame
            
        Returns:
            bool: True si debe continuar el juego, False si debe salir
        """
        for event in events:
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
                
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)
                
        return True
        
    def _handle_mouse_click(self, mouse_pos):
        """
        Maneja clicks del mouse.
        
        Args:
            mouse_pos (tuple): Posición (x, y) del click
        """
        # Verificar click en botón de dados
        dice_button_rect = pygame.Rect(800, 400, 120, 40)
        if dice_button_rect.collidepoint(mouse_pos) and not self.dice_rolled:
            self._roll_dice()
            return
            
        # Verificar click en tablero
        clicked_position = self.board_renderer.get_position_from_mouse(mouse_pos)
        if clicked_position is not None:
            self._handle_board_click(clicked_position)
            
    def _handle_board_click(self, position):
        """
        Maneja clicks en el tablero.
        
        Args:
            position (int): Posición clickeada (0-23)
        """
        if not self.dice_rolled:
            print("Primero debes tirar los dados")
            return
            
        # Si no hay posición seleccionada, seleccionar origen
        if self.selected_position is None:
            if self._can_select_position(position):
                self.selected_position = position
                print(f"Seleccionada posición {position}")
            else:
                print(f"No puedes seleccionar la posición {position}")
        else:
            # Ya hay origen seleccionado, intentar mover
            self._attempt_move(self.selected_position, position)
            self.selected_position = None
            
    def _can_select_position(self, position):
        """
        Verifica si una posición puede ser seleccionada como origen.
        
        Args:
            position (int): Posición a verificar
            
        Returns:
            bool: True si se puede seleccionar
        """
        try:
            tablero_state = self.game.estado_tablero()
            current_player_color = self.game.turno_actual.obtener_color()
            
            # Verificar si hay fichas del jugador actual
            if position < len(tablero_state):
                pieces_at_position = tablero_state[position]
                return len(pieces_at_position) > 0 and pieces_at_position[0] == current_player_color
                
        except Exception as e:
            print(f"Error verificando posición: {e}")
            
        return False
        
    def _attempt_move(self, origin, destination):
        """
        Intenta realizar un movimiento.
        
        Args:
            origin (int): Posición de origen
            destination (int): Posición de destino
        """
        try:
            # Verificar si el jugador tiene fichas en la barra
            current_player_color = self.game.turno_actual.obtener_color()
            fichas_barra = self.game.fichas_en_barra(current_player_color)
            
            if fichas_barra > 0:
                print("Debes reingresar las fichas de la barra primero")
                return
                
            # Calcular diferencia para validar con dados
            if current_player_color == "Blancas":
                dice_value = destination - origin
            else:
                dice_value = origin - destination
                
            # Verificar si el dado está disponible
            dados_disponibles = getattr(self.game, 'dados_actuales', [])
            if dice_value not in dados_disponibles:
                print(f"Movimiento de {dice_value} no disponible con dados actuales")
                return
                
            # Intentar el movimiento
            if self.game.mover(origin, destination):
                print(f"Movimiento exitoso de {origin} a {destination}")
                # Remover el dado usado
                if hasattr(self.game, 'dados_actuales'):
                    self.game.dados_actuales.remove(dice_value)
                    if not self.game.dados_actuales:
                        self._end_turn()
            else:
                print(f"Movimiento inválido de {origin} a {destination}")
                
        except Exception as e:
            print(f"Error en movimiento: {e}")
            
    def _roll_dice(self):
        """Tira los dados para el turno actual."""
        try:
            dados_valores = self.game.tirar_dados()
            self.game.dados_actuales = dados_valores.copy()
            self.dice_rolled = True
            
            current_player = self.game.turno_actual.obtener_nombre()
            print(f"{current_player} tiró: {dados_valores}")
            
            # Verificar si debe reingresar fichas
            current_player_color = self.game.turno_actual.obtener_color()
            fichas_barra = self.game.fichas_en_barra(current_player_color)
            
            if fichas_barra > 0:
                if not self.game.puede_reingresar():
                    print("No puedes reingresar fichas. Turno perdido.")
                    self._end_turn()
                else:
                    print("Debes reingresar fichas de la barra")
                    
        except Exception as e:
            print(f"Error tirando dados: {e}")
            
    def _handle_key_press(self, key):
        """
        Maneja pulsaciones de teclas.
        
        Args:
            key: Código de la tecla presionada
        """
        if key == pygame.K_SPACE:
            # Espacebar - tirar dados
            if not self.dice_rolled:
                self._roll_dice()
                
        elif key == pygame.K_ESCAPE:
            # Escape - limpiar selección
            self.selected_position = None
            print("Selección limpiada")
            
        elif key == pygame.K_RETURN:
            # Enter - pasar turno
            if self.dice_rolled:
                self._end_turn()
                
        elif key == pygame.K_r and pygame.key.get_pressed()[pygame.K_LCTRL]:
            # Ctrl+R - reiniciar juego
            self._restart_game()
            
    def _end_turn(self):
        """Termina el turno actual."""
        try:
            self.game.cambiar_turno()
            self.dice_rolled = False
            self.selected_position = None
            
            new_player = self.game.turno_actual.obtener_nombre()
            print(f"Turno de {new_player}")
            
            # Verificar si el juego terminó
            if self.game.juego_terminado():
                ganador = self.game.obtener_ganador()
                print(f"¡Juego terminado! Ganador: {ganador}")
                
        except Exception as e:
            print(f"Error cambiando turno: {e}")
            
    def _restart_game(self):
        """Reinicia el juego."""
        try:
            # Reinicializar estado del juego
            self.game.tablero.inicializar_piezas()
            self.dice_rolled = False
            self.selected_position = None
            print("Juego reiniciado")
            
        except Exception as e:
            print(f"Error reiniciando juego: {e}")
            
    def get_selected_position(self):
        """
        Obtiene la posición actualmente seleccionada.
        
        Returns:
            int or None: Posición seleccionada o None
        """
        return self.selected_position
        
    def is_dice_rolled(self):
        """
        Verifica si los dados ya fueron tirados en este turno.
        
        Returns:
            bool: True si los dados fueron tirados
        """
        return self.dice_rolled