#Revisar 

class jugador:
    def __init__(self, nombre: str, color: str):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = 15 # Total de fichas que tiene el jugador al inicio 
        self.__fichas_restantes__ = 15 # Fichas que le quedan por sacar del tablero (para ganar)
        self.__barra__ = 0 # Fichas que están en la barra (fueron comidas y deben reingresar)

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
        # Devuelve True si pudo sacar una ficha, False si no quedaban
        
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ -= 1
            return True
        return False

    def agregar_a_barra(self):
        # Agrega una ficha a la barra (cuando es comida por el oponente)
        self.__barra__ += 1

    def quitar_de_barra(self):
        
        # Quita una ficha de la barra (cuando el jugador reingresa una ficha al tablero)
        # Devuelve True si había fichas en la barra, False si no
        
        if self.__barra__ > 0:
            self.__barra__ -= 1
            return True
        return False

    def tiene_en_barra(self):
        # Devuelve True si el jugador tiene al menos una ficha en la barra
        return self.__barra__ > 0

    def __str__(self):
        return (f"Jugador: {self.__nombre__}, Color: {self.__color__}, "
                f"Fichas restantes: {self.__fichas_restantes__}, En barra: {self.__barra__}")