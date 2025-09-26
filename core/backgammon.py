# Backgammon: clase principal que coordina el flujo del juego.
# Integra tablero, jugadores y dados, y gestiona las reglas principales.

from core.tablero import tablero
from core.jugador import jugador
from core.dice import dice

class Backgammon:
    def __init__(self, nombre_jugador1, color_jugador1, nombre_jugador2, color_jugador2):
        """
        Inicializa el juego de Backgammon con dos jugadores, el tablero y los dados.
        """
        self.tablero = tablero()
        self.jugador1 = jugador(nombre_jugador1, color_jugador1)
        self.jugador2 = jugador(nombre_jugador2, color_jugador2)
        self.dados = dice()
        self.turno_actual = self.jugador1  # Por defecto empieza jugador1
        self.tablero.inicializar_piezas()
        self.dados_actuales = []

    def tirar_dados(self):
        """
        Llama al método de tirar los dados y guarda el resultado.
        Devuelve una lista con los valores de los dados.
        """
        self.dados_actuales = self.dados.tirar()
        return self.dados_actuales

    def cambiar_turno(self):
        """
        Cambia el turno al otro jugador.
        """
        if self.turno_actual == self.jugador1:
            self.turno_actual = self.jugador2
        else:
            self.turno_actual = self.jugador1

    def mover(self, origen, destino):
        """
        Intenta mover una pieza del jugador actual desde 'origen' a 'destino'.
        Devuelve True si el movimiento fue válido y realizado, False en caso contrario.
        """
        color = self.turno_actual.obtener_color()
        if self.tablero.validar_movimiento(origen, destino, color):
            self.tablero.mover_pieza(origen, destino)
            return True
        return False

    def puede_reingresar(self):
        """
        Verifica si el jugador actual puede reingresar fichas desde la barra con los dados actuales.
        """
        color = self.turno_actual.obtener_color()
        return self.tablero.puede_reingresar(color, self.dados_actuales)

    def reingresar_desde_barra(self, destino):
        """
        Intenta reingresar una ficha desde la barra al tablero en la posición 'destino'.
        Devuelve True si pudo reingresar, False si no.
        """
        color = self.turno_actual.obtener_color()
        return self.tablero.reingresar_desde_barra(color, destino)

    def fichas_en_barra(self, color=None):
        """
        Devuelve la cantidad de fichas en la barra del jugador actual o del color especificado.
        """
        if color is None:
            color = self.turno_actual.obtener_color()
        return self.tablero.fichas_en_barra(color)

    def todas_en_home(self):
        """
        Devuelve True si todas las fichas del jugador actual están en el home.
        """
        color = self.turno_actual.obtener_color()
        return self.tablero.todas_en_home(color)

    def sacar_ficha_fuera(self, origen):
        """
        Intenta sacar una ficha fuera del tablero desde la posición 'origen' para el jugador actual.
        Devuelve True si pudo sacar la ficha, False si no.
        """
        color = self.turno_actual.obtener_color()
        if self.tablero.sacar_ficha_fuera(color, origen):
            # Actualiza el estado del jugador
            self.turno_actual.sacar_ficha_a_afuera()
            return True
        return False

    def juego_terminado(self):
        """
        Verifica si algún jugador ganó (no le quedan fichas por sacar).
        """
        return self.jugador1.gano() or self.jugador2.gano()

    def obtener_ganador(self):
        """
        Devuelve el nombre del ganador si hay uno, o None si no hay ganador aún.
        """
        if self.jugador1.gano():
            return self.jugador1.obtener_nombre()
        elif self.jugador2.gano():
            return self.jugador2.obtener_nombre()
        return None

    def estado_tablero(self):
        """
        Devuelve el estado actual del tablero (para mostrar o debug).
        """
        return self.tablero.mostrar_tablero()

    def estado_jugador(self, jugador=None):
        """
        Devuelve información del jugador actual o del especificado.
        """
        if jugador is None:
            jugador = self.turno_actual
        return {
            "nombre": jugador.obtener_nombre(),
            "color": jugador.obtener_color(),
            "fichas_restantes": jugador.mostrar_fichas_restantes(),
            "en_barra": self.fichas_en_barra(jugador.obtener_color())
        }