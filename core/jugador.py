class jugador():
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color

    def __str__(self):
        return f"Jugador: {self.nombre}, Color: {self.color}"

    def __repr__(self):
        return f"Jugador(nombre={self.nombre}, color={self.color})"