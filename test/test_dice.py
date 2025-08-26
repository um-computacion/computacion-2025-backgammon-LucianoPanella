import unittest
from core.dice import Dice
import random

class TestDice(unittest.TestCase):

    def test_tirada_devuelve_lista(self):
        dado = Dice()
        resultado = dado.tirada()
        self.assertIsInstance(resultado, list, "El resultado debe ser una lista.")

    def test_valores_entre_1_y_6(self):
        dado = Dice()
        resultado = dado.tirada()
        for valor in resultado:
            self.assertTrue(1 <= valor <= 6, f"El valor {valor} no está entre 1 y 6.")

    def test_tirada_doble(self):
        dado = Dice()
        original_randint = random.randint
        random.randint = lambda a, b: 4
        resultado = dado.tirada()
        self.assertEqual(len(resultado), 4, "La tirada doble debe tener 4 valores.")
        self.assertTrue(all(v == 4 for v in resultado), "Todos los valores deben ser iguales en una tirada doble.")
        random.randint = original_randint

    def test_tirada_normal(self):
        dado = Dice()
        original_randint = random.randint
        valores = [2, 5]
        random.randint = lambda a, b: valores.pop(0)
        resultado = dado.tirada()
        self.assertEqual(len(resultado), 2, "Una tirada normal debe tener 2 valores.")
        self.assertEqual(resultado, [2, 5])
        random.randint = original_randint

    def test_obtener_ult_tirada_devuelve_ultima_tirada(self):
        dado = Dice()
        resultado = dado.tirada()
        self.assertEqual(dado.obtener_ult_tirada(), resultado, "get_last_roll debe devolver la última tirada.")

    def test_tirada_es_falso_al_inicio(self):
        dado = Dice()
        self.assertFalse(dado._ha_tirado, "Al inicio no debería haber tiradas.")

    def test_tirada_es_verdadero_despues_de_tirar(self):
        dado = Dice()
        dado.tirada()  
        resultado = dado.tirada()  
        self.assertTrue(resultado, "Después de tirar debería ser True.")


if __name__ == '__main__':
    unittest.main()