# Responsable de dibujar el tablero de juego y sus elementos
# como fichas, puntos y la barra central
# Se encarga de actualizar la visualizacion del tablero

import pygame
import math
from .constants import *

class BoardRenderer:
    def __init__(self, screen):
        """
        Inicializa el renderizador del tablero.
        
        Args:
            screen: Superficie de Pygame donde renderizar
        """
        self.screen = screen
        self.font_medium = pygame.font.Font(None, FONT_SIZES['MEDIUM'])
        self.font_small = pygame.font.Font(None, FONT_SIZES['SMALL'])
        
    def draw_board(self, tablero_state):
        """
        Dibuja el tablero completo.
        
        Args:
            tablero_state: Estado actual del tablero
        """
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Dibujar tablero base
        self._draw_board_base()
        
        # Dibujar triángulos
        self._draw_triangles()
        
        # Dibujar fichas
        self._draw_pieces(tablero_state)
        
        # Dibujar barra
        self._draw_bar(tablero_state)
        
        # Dibujar home
        self._draw_home(tablero_state)
        
        # Dibujar números de posición
        self._draw_position_numbers()
        
    def _draw_board_base(self):
        """Dibuja la estructura base del tablero."""
        # Tablero principal
        board_rect = pygame.Rect(
            BOARD_MARGIN, 
            BOARD_MARGIN, 
            12 * TRIANGLE_WIDTH + BAR_WIDTH, 
            2 * TRIANGLE_HEIGHT
        )
        pygame.draw.rect(self.screen, COLORS['BOARD_LIGHT'], board_rect)
        pygame.draw.rect(self.screen, COLORS['BORDER'], board_rect, 3)
        
        # Línea central
        center_y = BOARD_MARGIN + TRIANGLE_HEIGHT
        pygame.draw.line(
            self.screen, 
            COLORS['BORDER'],
            (BOARD_MARGIN, center_y),
            (BOARD_MARGIN + 12 * TRIANGLE_WIDTH + BAR_WIDTH, center_y),
            2
        )
        
    def _draw_triangles(self):
        """Dibuja los triángulos del tablero."""
        for i in range(24):
            self._draw_triangle(i)
            
    def _draw_triangle(self, position):
        """
        Dibuja un triángulo específico.
        
        Args:
            position (int): Posición del triángulo (0-23)
        """
        # Calcular posición y orientación
        if position < 12:
            # Triángulos superiores (posiciones 12-23 visualmente)
            visual_pos = 23 - position
            x = BOARD_MARGIN + (visual_pos % 6) * TRIANGLE_WIDTH
            if visual_pos >= 6:
                x += BAR_WIDTH
            y = BOARD_MARGIN
            pointing_down = True
        else:
            # Triángulos inferiores (posiciones 0-11 visualmente)
            visual_pos = position - 12
            x = BOARD_MARGIN + (5 - visual_pos % 6) * TRIANGLE_WIDTH
            if visual_pos < 6:
                x += BAR_WIDTH
            y = BOARD_MARGIN + TRIANGLE_HEIGHT
            pointing_down = False
            
        # Color alternado
        color = COLORS['BOARD_DARK'] if position % 2 == 0 else COLORS['BOARD_LIGHT']
        
        # Puntos del triángulo
        if pointing_down:
            points = [
                (x, y),
                (x + TRIANGLE_WIDTH, y),
                (x + TRIANGLE_WIDTH // 2, y + TRIANGLE_HEIGHT)
            ]
        else:
            points = [
                (x, y + TRIANGLE_HEIGHT),
                (x + TRIANGLE_WIDTH, y + TRIANGLE_HEIGHT),
                (x + TRIANGLE_WIDTH // 2, y)
            ]
            
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, COLORS['BORDER'], points, 2)
        
    def _draw_pieces(self, tablero_state):
        """
        Dibuja las fichas en el tablero.
        
        Args:
            tablero_state: Lista con el estado de cada posición
        """
        for position, pieces in enumerate(tablero_state):
            if pieces:
                self._draw_pieces_at_position(position, pieces)
                
    def _draw_pieces_at_position(self, position, pieces):
        """
        Dibuja fichas en una posición específica.
        
        Args:
            position (int): Posición en el tablero
            pieces (list): Lista de fichas en esa posición
        """
        # Calcular posición base
        if position < 12:
            visual_pos = 23 - position
            x = BOARD_MARGIN + (visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            if visual_pos >= 6:
                x += BAR_WIDTH
            base_y = BOARD_MARGIN + TRIANGLE_HEIGHT - PIECE_RADIUS
            direction = -1  # Hacia arriba
        else:
            visual_pos = position - 12
            x = BOARD_MARGIN + (5 - visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            if visual_pos < 6:
                x += BAR_WIDTH
            base_y = BOARD_MARGIN + TRIANGLE_HEIGHT + PIECE_RADIUS
            direction = 1  # Hacia abajo
            
        # Dibujar cada ficha
        for i, piece_color in enumerate(pieces):
            y = base_y + (direction * (i * (PIECE_RADIUS * 2 + PIECE_SPACING)))
            color = COLORS['WHITE_PIECE'] if piece_color == 'Blancas' else COLORS['BLACK_PIECE']
            
            pygame.draw.circle(self.screen, color, (int(x), int(y)), PIECE_RADIUS)
            pygame.draw.circle(self.screen, COLORS['BORDER'], (int(x), int(y)), PIECE_RADIUS, 2)
            
            # Si hay más de 5 fichas, mostrar número
            if len(pieces) > 5 and i == 4:
                text = self.font_small.render(str(len(pieces)), True, COLORS['TEXT'])
                text_rect = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rect)
                break
                
    def _draw_bar(self, tablero_state):
        """
        Dibuja la barra central con fichas capturadas.
        
        Args:
            tablero_state: Estado del tablero (debe incluir información de barra)
        """
        bar_x = BOARD_MARGIN + 6 * TRIANGLE_WIDTH + BAR_WIDTH // 2
        bar_rect = pygame.Rect(
            BOARD_MARGIN + 6 * TRIANGLE_WIDTH,
            BOARD_MARGIN,
            BAR_WIDTH,
            2 * TRIANGLE_HEIGHT
        )
        
        pygame.draw.rect(self.screen, COLORS['BOARD_DARK'], bar_rect)
        pygame.draw.rect(self.screen, COLORS['BORDER'], bar_rect, 2)
        
        # Texto "BAR"
        text = self.font_medium.render("BAR", True, COLORS['TEXT'])
        text_rect = text.get_rect(center=(bar_x, BOARD_MARGIN + TRIANGLE_HEIGHT))
        self.screen.blit(text, text_rect)
        
    def _draw_home(self, tablero_state):
        """
        Dibuja las áreas de home para fichas sacadas.
        
        Args:
            tablero_state: Estado del tablero
        """
        home_x = BOARD_MARGIN + 12 * TRIANGLE_WIDTH + BAR_WIDTH + 10
        
        # Home superior (Blancas)
        home_rect_white = pygame.Rect(home_x, BOARD_MARGIN, HOME_WIDTH, TRIANGLE_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['BOARD_LIGHT'], home_rect_white)
        pygame.draw.rect(self.screen, COLORS['BORDER'], home_rect_white, 2)
        
        text = self.font_small.render("HOME", True, COLORS['TEXT'])
        self.screen.blit(text, (home_x + 5, BOARD_MARGIN + 10))
        text = self.font_small.render("BLANCAS", True, COLORS['TEXT'])
        self.screen.blit(text, (home_x + 5, BOARD_MARGIN + 30))
        
        # Home inferior (Negras)
        home_rect_black = pygame.Rect(home_x, BOARD_MARGIN + TRIANGLE_HEIGHT, HOME_WIDTH, TRIANGLE_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['BOARD_DARK'], home_rect_black)
        pygame.draw.rect(self.screen, COLORS['BORDER'], home_rect_black, 2)
        
        text = self.font_small.render("HOME", True, COLORS['TEXT'])
        self.screen.blit(text, (home_x + 5, BOARD_MARGIN + TRIANGLE_HEIGHT + 10))
        text = self.font_small.render("NEGRAS", True, COLORS['TEXT'])
        self.screen.blit(text, (home_x + 5, BOARD_MARGIN + TRIANGLE_HEIGHT + 30))
        
    def _draw_position_numbers(self):
        """Dibuja los números de las posiciones."""
        for i in range(24):
            if i < 12:
                visual_pos = 23 - i
                x = BOARD_MARGIN + (visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
                if visual_pos >= 6:
                    x += BAR_WIDTH
                y = BOARD_MARGIN - 20
                number = str(i)
            else:
                visual_pos = i - 12
                x = BOARD_MARGIN + (5 - visual_pos % 6) * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
                if visual_pos < 6:
                    x += BAR_WIDTH
                y = BOARD_MARGIN + 2 * TRIANGLE_HEIGHT + 5
                number = str(i)
                
            text = self.font_small.render(number, True, COLORS['TEXT'])
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
            
    def get_position_from_mouse(self, mouse_pos):
        """
        Convierte posición del mouse a posición del tablero.
        
        Args:
            mouse_pos (tuple): Coordenadas (x, y) del mouse
            
        Returns:
            int or None: Posición del tablero o None si no está sobre una posición válida
        """
        x, y = mouse_pos
        
        # Verificar si está dentro del área del tablero
        if (x < BOARD_MARGIN or x > BOARD_MARGIN + 12 * TRIANGLE_WIDTH + BAR_WIDTH or
            y < BOARD_MARGIN or y > BOARD_MARGIN + 2 * TRIANGLE_HEIGHT):
            return None
            
        # Calcular posición aproximada
        relative_x = x - BOARD_MARGIN
        
        # Ajustar por la barra
        if relative_x > 6 * TRIANGLE_WIDTH + BAR_WIDTH:
            relative_x -= BAR_WIDTH
            section = 1
        else:
            section = 0
            
        triangle_index = int(relative_x // TRIANGLE_WIDTH)
        
        if y < BOARD_MARGIN + TRIANGLE_HEIGHT:
            # Parte superior
            if section == 0:
                position = 23 - triangle_index
            else:
                position = 17 - triangle_index
        else:
            # Parte inferior
            if section == 0:
                position = 12 + (5 - triangle_index)
            else:
                position = 6 + (5 - triangle_index)
                
        return position if 0 <= position <= 23 else None