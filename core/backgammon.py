#Revisar y completar el código, terminar de detallar las funciones
#Y agregar funciones necesarias para el juego

from core.tablero import tablero
from core.jugador import jugador
from core.dice import dice

class Backgammon:
    def __init__(self, nombre_jugador1, color_jugador1, nombre_jugador2, color_jugador2):
        # Inicializa el tablero, los jugadores y los dados
        self.tablero = tablero()
        self.jugador1 = jugador(nombre_jugador1, color_jugador1)
        self.jugador2 = jugador(nombre_jugador2, color_jugador2)
        self.dados = dice()
        self.turno_actual = self.jugador1  # Por defecto empieza jugador1

        # Inicializa las piezas en el tablero
        self.tablero.inicializar_piezas()

    def tirar_dados(self):
        # Llama al método de tirar los dados y devuelve el resultado
        return self.dados.tirar()

    def cambiar_turno(self):
        # Cambia el turno al otro jugador
        if self.turno_actual == self.jugador1:
            self.turno_actual = self.jugador2
        else:
            self.turno_actual = self.jugador1

    def mover(self, origen, destino):
        # Intenta mover una pieza del jugador actual
        color = self.turno_actual.obtener_color()
        if self.tablero.validar_movimiento(origen, destino, color):
            self.tablero.mover_pieza(origen, destino)
            return True
        return False

    def juego_terminado(self):
        # Verifica si algún jugador ganó
        return self.jugador1.gano() or self.jugador2.gano()

    def obtener_ganador(self):
        # Devuelve el nombre del ganador si hay uno
        if self.jugador1.gano():
            return self.jugador1.obtener_nombre()
        elif self.jugador2.gano():
            return self.jugador2.obtener_nombre()
        return None