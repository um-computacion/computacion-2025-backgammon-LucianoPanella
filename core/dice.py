#Revisar

import random

class dice:
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
        # Método alternativo, mantiene compatibilidad si lo usas en otro lado
        if not self._ha_tirado:
            return self.tirar()
        else:
            return True

    def obtener_ult_tirada(self):
        return self._ultima_tirada