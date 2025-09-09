#Revisar

class tablero:
    def __init__(self):
        # Inicializa el tablero con 24 posiciones vacías (listas)
        self.__tablero__ = [[] for _ in range(24)]
        # Contador de piezas comidas
        self.__piezas_comidas__ = {"Blancas": 0, "Negras": 0}

    def inicializar_piezas(self):
        # Coloca las piezas en las posiciones iniciales estándar
        self.__tablero__ = [[] for _ in range(24)]
        self.__tablero__[0] = ["Blancas"] * 2
        self.__tablero__[5] = ["Negras"] * 5
        self.__tablero__[7] = ["Negras"] * 3
        self.__tablero__[11] = ["Blancas"] * 5
        self.__tablero__[12] = ["Negras"] * 5
        self.__tablero__[16] = ["Blancas"] * 3
        self.__tablero__[18] = ["Blancas"] * 5
        self.__tablero__[23] = ["Negras"] * 2

    def mostrar_tablero(self):
        # Devuelve el estado actual del tablero
        return self.__tablero__

    def piezas_comidas(self):
        # Devuelve el diccionario de piezas comidas
        return self.__piezas_comidas__

    def sacar_pieza(self, posicion: int):
        # Saca una pieza de la posición indicada (si hay)
        if self.__tablero__[posicion]:
            return self.__tablero__[posicion].pop()
        return None

    def colocar_pieza(self, posicion: int, color: str):
        # Coloca una pieza del color dado en la posición indicada
        self.__tablero__[posicion].append(color)

    def mover_pieza(self, origen: int, destino: int):
        # Mueve una pieza del origen al destino si es posible
        if not self.__tablero__[origen]:
            raise ValueError("No hay piezas para mover en la posición de origen.")
        pieza = self.sacar_pieza(origen)
        # Si hay una sola pieza enemiga en destino, la come
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != pieza and
            len(self.__tablero__[destino]) == 1):
            color_comido = self.__tablero__[destino].pop()
            self.__piezas_comidas__[color_comido] += 1
        self.colocar_pieza(destino, pieza)

    def validar_movimiento(self, origen: int, destino: int, color: str):
        # Valida si un movimiento es posible según las reglas básicas
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            return False
        if not self.__tablero__[origen]:
            return False
        if self.__tablero__[origen][-1] != color:
            return False
        # No puede mover a una posición con 2 o más piezas enemigas
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != color and
            len(self.__tablero__[destino]) > 1):
            return False
        return True
