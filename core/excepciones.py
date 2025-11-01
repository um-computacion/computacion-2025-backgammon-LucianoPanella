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
    

class PosicionFueraDeRango(BackgammonError):
    """La posición indicada está fuera del tablero."""
    

class OrigenSinFicha(BackgammonError):
    """No hay ficha en la posición de origen."""
    

class DestinoBloqueado(BackgammonError):
    """No se puede mover a la posición de destino porque está bloqueada por el rival."""
    

class NoPuedeReingresar(BackgammonError):
    """No se puede reingresar ficha desde la barra en la posición indicada."""
    

class NoPuedeSacarFicha(BackgammonError):
    """No se puede sacar ficha fuera del tablero (no todas en home o dado incorrecto)."""
    

#Excepciones para Jugador

class FichaNoDisponible(BackgammonError):
    """El jugador no tiene fichas disponibles para la acción solicitada."""
    

class JugadorYaGano(BackgammonError):
    """El jugador ya ha ganado, no puede realizar más movimientos."""
    

#Excepciones para Dados

class DadosNoTirados(BackgammonError):
    """Se intentó usar los dados antes de tirarlos."""
    

class DadoNoDisponible(BackgammonError):
    """El dado seleccionado no está disponible para este turno."""
    

#Excepciones para Juego

class TurnoIncorrecto(BackgammonError):
    """No es el turno del jugador que intenta mover."""
    

class JuegoYaTerminado(BackgammonError):
    """Se intentó realizar una acción cuando el juego ya terminó."""
    

# Excepciones para CLI / Entrada de usuario

class EntradaInvalida(BackgammonError):
    """La entrada recibida no cumple el formato o rango esperado."""
    

class OpcionInvalida(BackgammonError):
    """La opción de menú seleccionada no es válida en este contexto."""
    

class DebeReingresarPrimero(BackgammonError):
    """El jugador tiene fichas en barra y debe reingresar antes de mover otras fichas."""
    

class NoHayReingresoPosible(BackgammonError):
    """Con los dados disponibles no existe ninguna entrada válida desde la barra."""
    

class SinMovimientosDisponibles(BackgammonError):
    """No existe ningún movimiento legal con los dados disponibles."""
    