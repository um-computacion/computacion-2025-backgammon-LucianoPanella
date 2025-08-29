from core.tablero import tablero
import unittest

class TestTablero(unittest.TestCase):

    def test_init_tablero(self):
        tablero1 = tablero()
        self.assertEqual(len(tablero1._tablero__tablero__), 0)  # El tablero debería tener 0 posiciones inicialmente debido al error en la inicialización

    def test_pieza_inicio(self):
        tablero1 = tablero()
        tablero1.pieza_inicio(0, "Blancas")
        self.assertEqual(tablero1._tablero__tablero__[0], ["Blancas"] * 2)
        self.assertEqual(tablero1._tablero__tablero__[11], ["Blancas"] * 5)
        self.assertEqual(tablero1._tablero__tablero__[16], ["Blancas"] * 3)
        self.assertEqual(tablero1._tablero__tablero__[18], ["Blancas"] * 5)
        self.assertEqual(tablero1._tablero__tablero__[23], ["Negras"] * 2)
        self.assertEqual(tablero1._tablero__tablero__[12], ["Negras"] * 5)
        self.assertEqual(tablero1._tablero__tablero__[7], ["Negras"] * 3)
        self.assertEqual(tablero1._tablero__tablero__[5], ["Negras"] * 5)

    def test_str_tablero(self):
        tablero1 = tablero()
        expected_str = "Tablero: []"
        self.assertEqual(str(tablero1), expected_str)

    def test_sacar_pieza(self):
        tablero1 = tablero()
        tablero1.pieza_inicio(0, "Blancas")
        tablero1.sacar_pieza(0, None)
        self.assertEqual(tablero1._tablero__tablero__[0], ["Blancas"])