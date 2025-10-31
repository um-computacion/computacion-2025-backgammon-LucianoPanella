# Backgammon: clase principal que coordina el flujo del juego.
# Integra tablero, jugadores y dados, y gestiona las reglas principales.

from core.tablero import tablero
from core.jugador import jugador
from core.dice import dice
from core.excepciones import TurnoIncorrecto, JuegoYaTerminado

class Backgammon:
    def __init__(
        self,
        nombre_jugador1,
        color_jugador1,
        nombre_jugador2,
        color_jugador2,
        *,
        tablero_inst=None,
        dados_inst=None,
        jugador1_inst=None,
        jugador2_inst=None,
    ):
        """
        Inicializa el juego de Backgammon con dos jugadores, el tablero y los dados.

    Dependency Inversion + Inyección de Dependencias:
        - Se aceptan instancias para tablero, dados y jugadores vía parámetros opcionales.
        - Razón: desacoplar Backgammon de implementaciones concretas y facilitar testing.
        """
        # Usamos instancias inyectadas con valores por defecto.
        self.tablero = tablero_inst if tablero_inst is not None else tablero()
        self.jugador1 = jugador1_inst if jugador1_inst is not None else jugador(nombre_jugador1, color_jugador1)
        self.jugador2 = jugador2_inst if jugador2_inst is not None else jugador(nombre_jugador2, color_jugador2)
        self.dados = dados_inst if dados_inst is not None else dice()
        self.turno_actual = self.jugador1  # Por defecto empieza jugador1
        self.tablero.inicializar_piezas()
        self.dados_actuales = []
        self._juego_terminado = False

    def tirar_dados(self):
        """
        Llama al método de tirar los dados y guarda el resultado.
        Devuelve una lista con los valores de los dados.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado, no se pueden tirar más dados.")
        
        self.dados_actuales = self.dados.tirar()
        return self.dados_actuales

    def cambiar_turno(self):
        """
        Cambia el turno al otro jugador.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado, no se puede cambiar de turno.")
        
        if self.turno_actual == self.jugador1:
            self.turno_actual = self.jugador2
        else:
            self.turno_actual = self.jugador1
        
        # Reinicia el estado de los dados para el nuevo turno
        self.dados.reiniciar_turno()

    def mover(self, origen, destino):
        """
        Intenta mover una pieza del jugador actual desde 'origen' a 'destino'.
        Devuelve True si el movimiento fue válido y realizado.
        Lanza excepciones de dominio si el movimiento es inválido.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado, no se pueden realizar más movimientos.")
        
        color = self.turno_actual.obtener_color()
    # Validación y movimiento delegados al tablero; las condiciones inválidas se expresan con excepciones.
        self.tablero.validar_movimiento(origen, destino, color)
        self.tablero.mover_pieza(origen, destino)
        # Verificar si el juego terminó después del movimiento
        self._verificar_fin_juego()
        return True

    def puede_reingresar(self):
        """
        Verifica si el jugador actual puede reingresar fichas desde la barra con los dados actuales.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado.")
        
        color = self.turno_actual.obtener_color()
        return self.tablero.puede_reingresar(color, self.dados_actuales)

    def reingresar_desde_barra(self, destino):
        """
        Intenta reingresar una ficha desde la barra al tablero en la posición 'destino'.
        Devuelve True si pudo reingresar, False si no.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado, no se pueden reingresar fichas.")
        
        color = self.turno_actual.obtener_color()
        resultado = self.tablero.reingresar_desde_barra(color, destino)
        if resultado:
            self._verificar_fin_juego()
        return resultado

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
        Devuelve True si pudo sacar la ficha.
        Lanza excepciones si no es posible según reglas.
        """
        if self._juego_terminado:
            raise JuegoYaTerminado("El juego ya ha terminado, no se pueden sacar más fichas.")
        
        color = self.turno_actual.obtener_color()
    # Delegamos la regla de "todas en home" y operación de extracción al tablero.
        self.tablero.sacar_ficha_fuera(color, origen)
        # Actualiza el estado del jugador
    # El jugador administra su contador de fichas restantes.
        self.turno_actual.sacar_ficha_a_afuera()
        # Verificar si el juego terminó después de sacar la ficha
        self._verificar_fin_juego()
        return True

    def _verificar_fin_juego(self):
        """
        Método privado para verificar si el juego ha terminado después de cada acción.
        """
        if self.jugador1.gano() or self.jugador2.gano():
            self._juego_terminado = True

    def juego_terminado(self):
        """
        Verifica si algún jugador ganó (no le quedan fichas por sacar).
        """
        return self._juego_terminado or self.jugador1.gano() or self.jugador2.gano()

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

    def estado_tablero_visual(self):
        """
        Devuelve el estado visual del tablero (para mostrar en formato gráfico).
        """
        return self.tablero.mostrar_tablero_visual()

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
    
    def validar_turno_jugador(self, jugador_solicitado):
        """
        Valida si es el turno del jugador especificado.
        """
        if jugador_solicitado != self.turno_actual:
            raise TurnoIncorrecto(f"No es el turno de {jugador_solicitado.obtener_nombre()}. "
                                f"Es el turno de {self.turno_actual.obtener_nombre()}.")
        return True