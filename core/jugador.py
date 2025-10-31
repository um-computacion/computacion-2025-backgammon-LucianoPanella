#Revisar 
from core.excepciones import FichaNoDisponible, JugadorYaGano
from core.constants import INITIAL_CHECKERS

class jugador:
    def __init__(self, nombre: str, color: str):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = INITIAL_CHECKERS  # Total de fichas que tiene el jugador al inicio 
        self.__fichas_restantes__ = INITIAL_CHECKERS  # Fichas que le quedan por sacar del tablero (para ganar)

    def mostrar_fichas_restantes(self):
        # Devuelve la cantidad de fichas que le quedan al jugador por sacar del tablero
        return self.__fichas_restantes__

    def obtener_nombre(self):
       # Devuelve el nombre del jugador
        return self.__nombre__

    def obtener_color(self):
        # Devuelve el color de las fichas del jugador
        return self.__color__

    def gano(self):
        # Devuelve True si el jugador ya no tiene fichas restantes (osea que ganó)
        return self.__fichas_restantes__ == 0

    def sacar_ficha_a_afuera(self):
        # Resta una ficha de las fichas restantes (cuando el jugador saca una ficha del tablero).
        
        # Devuelve True si pudo sacar una ficha.
        if self.gano():
            raise JugadorYaGano("El jugador ya ha ganado, no puede sacar más fichas.")
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ -= 1
            return True
        else:
            raise FichaNoDisponible("No hay fichas disponibles para sacar del tablero.")

    def __str__(self):
        return (f"Jugador: {self.__nombre__}, Color: {self.__color__}, "
                f"Fichas restantes: {self.__fichas_restantes__}")