import unittest
from core.tablero import tablero

class TestTablero(unittest.TestCase):

    def setUp(self):
        self.tablero = tablero()

    def test_tablero_inicial_vacio(self):
        self.assertEqual(len(self.tablero.mostrar_tablero()), 24)
        for punto in self.tablero.mostrar_tablero():
            self.assertEqual(punto, [])

    def test_inicializar_piezas(self):
        self.tablero.inicializar_piezas()
        t = self.tablero.mostrar_tablero()
        self.assertEqual(t[0], ["Blancas"] * 2)
        self.assertEqual(t[5], ["Negras"] * 5)
        self.assertEqual(t[7], ["Negras"] * 3)
        self.assertEqual(t[11], ["Blancas"] * 5)
        self.assertEqual(t[12], ["Negras"] * 5)
        self.assertEqual(t[16], ["Blancas"] * 3)
        self.assertEqual(t[18], ["Blancas"] * 5)
        self.assertEqual(t[23], ["Negras"] * 2)

    def test_colocar_y_sacar_pieza(self):
        self.tablero.colocar_pieza(0, "Blancas")
        self.assertEqual(self.tablero.mostrar_tablero()[0], ["Blancas"])
        pieza = self.tablero.sacar_pieza(0)
        self.assertEqual(pieza, "Blancas")
        self.assertEqual(self.tablero.mostrar_tablero()[0], [])

    def test_sacar_pieza_vacia(self):
        pieza = self.tablero.sacar_pieza(5)
        self.assertIsNone(pieza)

    def test_mover_pieza_simple(self):
        self.tablero.colocar_pieza(0, "Blancas")
        self.tablero.mover_pieza(0, 1)
        self.assertEqual(self.tablero.mostrar_tablero()[0], [])
        self.assertEqual(self.tablero.mostrar_tablero()[1], ["Blancas"])

    def test_mover_pieza_comer(self):
        self.tablero.colocar_pieza(0, "Blancas")
        self.tablero.colocar_pieza(1, "Negras")
        self.tablero.mover_pieza(0, 1)
        self.assertEqual(self.tablero.mostrar_tablero()[0], [])
        self.assertEqual(self.tablero.mostrar_tablero()[1], ["Blancas"])
        self.assertEqual(self.tablero.piezas_comidas()["Negras"], 1)

    def test_mover_pieza_origen_vacio(self):
        with self.assertRaises(ValueError):
            self.tablero.mover_pieza(0, 1)

    def test_validar_movimiento_basico(self):
        self.tablero.colocar_pieza(0, "Blancas")
        self.assertTrue(self.tablero.validar_movimiento(0, 1, "Blancas"))
        self.assertFalse(self.tablero.validar_movimiento(0, 25, "Blancas"))  # destino fuera de rango
        self.assertFalse(self.tablero.validar_movimiento(1, 2, "Blancas"))   # origen vacío

    def test_validar_movimiento_enemigos(self):
        self.tablero.colocar_pieza(0, "Blancas")
        self.tablero.colocar_pieza(1, "Negras")
        self.tablero.colocar_pieza(1, "Negras")
        self.assertFalse(self.tablero.validar_movimiento(0, 1, "Blancas"))  # dos enemigas en destino

if __name__ == "__main__":
    unittest.main()