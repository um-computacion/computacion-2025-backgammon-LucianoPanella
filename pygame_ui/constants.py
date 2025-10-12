#Almacen de Variables Globales fijas relacionadas con el aspecto visual 
# y funcional de los elementos UI

import pygame

# Dimensiones de pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colores
COLORS = {
    'BACKGROUND': (139, 69, 19),      # Marrón tablero
    'BOARD_DARK': (101, 67, 33),     # Triángulos oscuros
    'BOARD_LIGHT': (222, 184, 135),  # Triángulos claros
    'BORDER': (0, 0, 0),             # Bordes negros
    'WHITE_PIECE': (255, 255, 255),   # Fichas blancas
    'BLACK_PIECE': (50, 50, 50),      # Fichas negras
    'SELECTED': (255, 255, 0),        # Pieza seleccionada
    'VALID_MOVE': (0, 255, 0),        # Movimiento válido
    'TEXT': (255, 255, 255),          # Texto blanco
    'BUTTON': (70, 130, 180),         # Botones
    'BUTTON_HOVER': (100, 149, 237),  # Botón hover
    'DICE_BG': (255, 255, 255),       # Fondo dados
    'DICE_DOTS': (0, 0, 0),           # Puntos dados
}

# Dimensiones del tablero
BOARD_MARGIN = 50
TRIANGLE_WIDTH = 50
TRIANGLE_HEIGHT = 150
PIECE_RADIUS = 20
PIECE_SPACING = 5

# Posiciones específicas
BAR_WIDTH = 60
HOME_WIDTH = 80
DICE_SIZE = 40

# Fuentes
FONT_SIZES = {
    'SMALL': 16,
    'MEDIUM': 24,
    'LARGE': 32,
}

