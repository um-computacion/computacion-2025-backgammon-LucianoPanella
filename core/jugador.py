class jugador():
    def __init__(self, nombre: str, color: str):
        self.__nombre__ = nombre
        self.__color__ = color

    def __str__(self):
        return f"Jugador: {self.__nombre__}, Color: {self.__color__}"