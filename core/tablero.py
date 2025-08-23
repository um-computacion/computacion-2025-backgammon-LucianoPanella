class tablero():
    def __init__(self, color):
        self.color = color
        self.casillas = [0] * 24  # Inicializa las 24 casillas del tablero

    def __str__(self):
        return f"Tablero de color {self.color} con casillas: {self.casillas}"

    def __repr__(self):
        return f"Tablero(color={self.color}, casillas={self.casillas})"

