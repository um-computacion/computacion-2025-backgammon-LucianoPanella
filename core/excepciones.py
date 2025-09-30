#Excepcion BackGammon

class BackgammonError(Exception):
    """Excepción base para el juego Backgammon."""
    pass

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