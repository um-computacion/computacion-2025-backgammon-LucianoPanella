import unittest
from core.dice import dice
import random

class TestDice(unittest.TestCase):

    def test_tirar_devuelve_lista(self):
        dado = dice()
        resultado = dado.tirar()
        self.assertIsInstance(resultado, list, "El resultado debe ser una lista.")

    def test_valores_entre_1_y_6(self):
        dado = dice()
        resultado = dado.tirar()
        for valor in resultado:
            self.assertTrue(1 <= valor <= 6, f"El valor {valor} no está entre 1 y 6.")

    def test_tirada_doble(self):
        dado = dice()
        original_randint = random.randint
        random.randint = lambda a, b: 4
        resultado = dado.tirar()
        self.assertEqual(len(resultado), 4, "La tirada doble debe tener 4 valores.")
        self.assertTrue(all(v == 4 for v in resultado), "Todos los valores deben ser iguales en una tirada doble.")
        random.randint = original_randint

    def test_tirada_normal(self):
        dado = dice()
        original_randint = random.randint
        valores = [2, 5]
        random.randint = lambda a, b: valores.pop(0)
        resultado = dado.tirar()
        self.assertEqual(len(resultado), 2, "Una tirada normal debe tener 2 valores.")
        self.assertEqual(resultado, [2, 5])
        random.randint = original_randint

    def test_obtener_ult_tirada_devuelve_ultima_tirada(self):
        dado = dice()
        resultado = dado.tirar()
        self.assertEqual(dado.obtener_ult_tirada(), resultado, "obtener_ult_tirada debe devolver la última tirada.")

    def test_ha_tirado_es_falso_al_inicio(self):
        dado = dice()
        self.assertFalse(dado._ha_tirado, "Al inicio no debería haber tiradas.")

    def test_ha_tirado_es_verdadero_despues_de_tirar(self):
        dado = dice()
        dado.tirar()
        self.assertTrue(dado._ha_tirado, "Después de tirar debería ser True.")

if __name__ == '__main__':
    unittest.main()