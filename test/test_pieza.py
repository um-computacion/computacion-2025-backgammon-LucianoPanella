import unittest
from core.pieza import pieza

class TestPieza(unittest.TestCase):

    def test_init_pieza(self):
        pieza1 = pieza("Blancas")
        self.assertEqual(pieza1.__color__, "Blancas")

    def test_str_pieza(self):
        pieza1 = pieza("Negras")
        expected_str = "Pieza de color: Negras"
        self.assertEqual(str(pieza1), expected_str)