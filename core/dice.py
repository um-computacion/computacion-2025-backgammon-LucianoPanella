#Revisar
#
import random

class dice:
    def __init__(self):
        self._ultima_tirada = []
        self._ha_tirado = False
    
    def tirada(self):

        if not self._ha_tirado: #Lanzo primera vez los dados
            valor1 = random.randint(1, 6)
            valor2 = random.randint(1, 6)
            
            if valor1 == valor2:
                resultado = [valor1, valor2, valor1, valor2]
            else:
                resultado = [valor1, valor2]
            
            # Guard0 la última tirada
            self._ultima_tirada = resultado
            self._ha_tirado = True
            
            return resultado
        else:
            return True
    
    def obtener_ult_tirada(self):

        return self._ultima_tirada