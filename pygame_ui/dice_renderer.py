# Responsable de dibujar los dados y el resultado de la tirada
# Se mostrara los dados antes de la tirada
# y luego el resultado de la tirada en la pantalla principal


import pygame
import math
from .constants import *

class DiceRenderer:
    def __init__(self, screen):
        """
        Inicializa el renderizador de dados.
        
        Args:
            screen: Superficie de Pygame donde renderizar
        """
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZES['MEDIUM'])
        
    def draw_dice(self, dice_values, position=(800, 300)):
        """
        Dibuja los dados con sus valores.
        
        Args:
            dice_values (list): Valores de los dados
            position (tuple): Posición base para dibujar
        """
        if not dice_values:
            return
            
        x, y = position
        
        for i, value in enumerate(dice_values):
            dice_x = x + i * (DICE_SIZE + 10)
            self._draw_single_die(dice_x, y, value)
            
        # Título
        text = self.font.render("Dados:", True, COLORS['TEXT'])
        self.screen.blit(text, (x, y - 30))
        
    def _draw_single_die(self, x, y, value):
        """
        Dibuja un dado individual.
        
        Args:
            x, y (int): Posición del dado
            value (int): Valor del dado (1-6)
        """
        # Fondo del dado
        dice_rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
        pygame.draw.rect(self.screen, COLORS['DICE_BG'], dice_rect)
        pygame.draw.rect(self.screen, COLORS['BORDER'], dice_rect, 2)
        
        # Dibujar puntos según el valor
        self._draw_dice_dots(x, y, value)
        
    def _draw_dice_dots(self, x, y, value):
        """
        Dibuja los puntos del dado según su valor.
        
        Args:
            x, y (int): Posición base del dado
            value (int): Valor del dado
        """
        dot_radius = 3
        center_x = x + DICE_SIZE // 2
        center_y = y + DICE_SIZE // 2
        
        # Posiciones de los puntos
        positions = {
            1: [(center_x, center_y)],
            2: [(x + 10, y + 10), (x + 30, y + 30)],
            3: [(x + 8, y + 8), (center_x, center_y), (x + 32, y + 32)],
            4: [(x + 10, y + 10), (x + 30, y + 10), (x + 10, y + 30), (x + 30, y + 30)],
            5: [(x + 8, y + 8), (x + 32, y + 8), (center_x, center_y), (x + 8, y + 32), (x + 32, y + 32)],
            6: [(x + 8, y + 8), (x + 32, y + 8), (x + 8, y + 20), (x + 32, y + 20), (x + 8, y + 32), (x + 32, y + 32)]
        }
        
        for dot_x, dot_y in positions.get(value, []):
            pygame.draw.circle(self.screen, COLORS['DICE_DOTS'], (dot_x, dot_y), dot_radius)
            
    def draw_roll_button(self, position=(800, 400), enabled=True):
        """
        Dibuja el botón para tirar dados.
        
        Args:
            position (tuple): Posición del botón
            enabled (bool): Si el botón está habilitado
        """
        x, y = position
        button_rect = pygame.Rect(x, y, 120, 40)
        
        color = COLORS['BUTTON'] if enabled else COLORS['BOARD_DARK']
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, COLORS['BORDER'], button_rect, 2)
        
        text_color = COLORS['TEXT'] if enabled else COLORS['BOARD_LIGHT']
        text = self.font.render("Tirar Dados", True, text_color)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        
        return button_rect  # Retornar para detección de clicks