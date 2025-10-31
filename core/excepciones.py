#FINALIZADO#
"""
Excepciones del dominio Backgammon segregadas en un módulo dedicado.
Razón: evitar mezclar lógica de reglas/casos de uso con definiciones de errores, mejorando cohesión y reusabilidad.
"""

#Excepcion BackGammon

class BackgammonError(Exception):
    """Excepción base para el juego Backgammon con mensaje accesible."""
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message

#Excepciones para Tablero

class MovimientoInvalido(BackgammonError):
    """El movimiento solicitado no es válido según las reglas."""
    pass

class PosicionFueraDeRango(BackgammonError):
    """La posición indicada está fuera del tablero."""
    pass

class OrigenSinFicha(BackgammonError):
    """No hay ficha en la posición de origen."""
    pass

class DestinoBloqueado(BackgammonError):
    """No se puede mover a la posición de destino porque está bloqueada por el rival."""
    pass

class NoPuedeReingresar(BackgammonError):
    """No se puede reingresar ficha desde la barra en la posición indicada."""
    pass

class NoPuedeSacarFicha(BackgammonError):
    """No se puede sacar ficha fuera del tablero (no todas en home o dado incorrecto)."""
    pass

#Excepciones para Jugador

class FichaNoDisponible(BackgammonError):
    """El jugador no tiene fichas disponibles para la acción solicitada."""
    pass

class JugadorYaGano(BackgammonError):
    """El jugador ya ha ganado, no puede realizar más movimientos."""
    pass

#Excepciones para Dados

class DadosNoTirados(BackgammonError):
    """Se intentó usar los dados antes de tirarlos."""
    pass

class DadoNoDisponible(BackgammonError):
    """El dado seleccionado no está disponible para este turno."""
    pass

#Excepciones para Juego

class TurnoIncorrecto(BackgammonError):
    """No es el turno del jugador que intenta mover."""
    pass

class JuegoYaTerminado(BackgammonError):
    """Se intentó realizar una acción cuando el juego ya terminó."""
    pass

# Excepciones para CLI / Entrada de usuario

class EntradaInvalida(BackgammonError):
    """La entrada recibida no cumple el formato o rango esperado."""
    pass

class OpcionInvalida(BackgammonError):
    """La opción de menú seleccionada no es válida en este contexto."""
    pass

class DebeReingresarPrimero(BackgammonError):
    """El jugador tiene fichas en barra y debe reingresar antes de mover otras fichas."""
    pass

class NoHayReingresoPosible(BackgammonError):
    """Con los dados disponibles no existe ninguna entrada válida desde la barra."""
    pass

class SinMovimientosDisponibles(BackgammonError):
    """No existe ningún movimiento legal con los dados disponibles."""
    pass