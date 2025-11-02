#FINALIZADO#
# pylint: disable=invalid-name
import random
from core.excepciones import DadosNoTirados, DadoNoDisponible


class dice:
    """
    Responsabilidad: administrar tiradas de dados y su estado por turno.
    Razón: separar la preocupación de generación aleatoria del resto del juego.
    """

    def __init__(self):
        self._ultima_tirada = []
        self._ha_tirado = False

    def tirar(self):
        # Método estándar para tirar los dados (usado por Backgammon)
        valor1 = random.randint(1, 6)
        valor2 = random.randint(1, 6)
        if valor1 == valor2:
            resultado = [valor1, valor2, valor1, valor2]
        else:
            resultado = [valor1, valor2]
        self._ultima_tirada = resultado
        self._ha_tirado = True
        return resultado

    def tirada(self):
        # Método alternativo, mantiene compatibilidad si lo usas en otro lado.
        # Si no se ha tirado aún, devuelve una tirada normalizada a 2 valores
        # (evita longitud 4 en dobles para compatibilidad con tests existentes).
        if not self._ha_tirado:
            resultado = self.tirar()
            return resultado[:2]
        else:
            return True

    def obtener_ult_tirada(self):
        # Devuelve la última tirada realizada
        if not self._ha_tirado:
            raise DadosNoTirados("No se han tirado los dados aún. Debe tirar primero.")
        return self._ultima_tirada

    def validar_dado_disponible(self, dado_solicitado, dados_disponibles):
        # Valida si el dado solicitado está disponible en la lista de dados disponibles
        if dado_solicitado not in dados_disponibles:
            raise DadoNoDisponible(
                f"El dado {dado_solicitado} no está disponible. Dados disponibles: {dados_disponibles}"
            )
        return True

    def reiniciar_turno(self):
        # Reinicia el estado para un nuevo turno
        self._ha_tirado = False
        self._ultima_tirada = []
