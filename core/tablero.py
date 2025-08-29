# Terminar de definir la validacion de movimientos
# y definir la funcion mover pieza
#
class tablero:

    def __init__(self): #Creo tablero con 24 posiciones
        self.__tablero__ = [] * 24
 

    def pieza_inicio(self, posicion: int, color: str): #Defino las piezas iniciales en su posicion correspondiente
        self.__tablero__[0] = ["Blancas"] * 2
        self.__tablero__[5] = ["Negras"] * 5
        self.__tablero__[7] = ["Negras"] * 3
        self.__tablero__[11] = ["Blancas"] * 5
        self.__tablero__[12] = ["Negras"] * 5 
        self.__tablero__[16] = ["Blancas"] * 3
        self.__tablero__[18] = ["Blancas"] * 5
        self.__tablero__[23] = ["Negras"] * 2
        
    def pieza_comida(self):
         self.__pieza_comida__ = {"Blancas": 0, "Negras": 0}
         return self.__Pieza_comida__

    def sacar_pieza(self, posicion: int, pieza_comida): #Saco una pieza del tablero
        if self.__tablero__[posicion]:
            self.__tablero__[posicion].pop() 

    def mostrar_tablero(self): #Muestro el tablero  
        return self.__tablero__ 


