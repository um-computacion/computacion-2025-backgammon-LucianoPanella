#FINALIZADO#
"""
Constantes del juego Backgammon.

Convención: todas las constantes en MAYÚSCULAS.
"""

# Colores
BLANCAS = "Blancas"
NEGRAS = "Negras"

# Tablero
BOARD_POINTS = 24  # número de posiciones (0..23)

# Setup inicial: posición -> (color, cantidad)
START_SETUP = {
    0: (BLANCAS, 2),
    5: (NEGRAS, 5),
    7: (NEGRAS, 3),
    11: (BLANCAS, 5),
    12: (NEGRAS, 5),
    16: (BLANCAS, 3),
    18: (BLANCAS, 5),
    23: (NEGRAS, 2),
}

# Fichas por jugador al inicio
INITIAL_CHECKERS = 15

# Rangos de home por color
HOME_RANGE = {
    BLANCAS: range(18, 24),
    NEGRAS: range(0, 6),
}

# Representación visual
MAX_STACK_DISPLAY_ROWS = 5
