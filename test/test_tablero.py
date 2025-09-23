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

    def test_reingresar_desde_barra(self):
        self.tablero.inicializar_piezas()
        self.tablero._tablero__barra__ = {"Blancas": 1, "Negras": 0}
        destino = 1
        self.assertTrue(self.tablero.reingresar_desde_barra("Blancas", destino))
        self.assertEqual(self.tablero.fichas_en_barra("Blancas"), 0)
        self.assertIn("Blancas", self.tablero.mostrar_tablero()[destino])

    def test_no_reingresa_si_barra_vacia(self):
        self.tablero.inicializar_piezas()
        self.tablero._tablero__barra__ = {"Blancas": 0, "Negras": 0}
        self.assertFalse(self.tablero.reingresar_desde_barra("Blancas", 1))

    def test_puede_reingresar(self):
        self.tablero.inicializar_piezas()
        self.tablero._tablero__barra__ = {"Blancas": 1, "Negras": 0}
        self.assertTrue(self.tablero.puede_reingresar("Blancas", [1]))
        self.tablero.colocar_pieza(0, "Negras")
        self.tablero.colocar_pieza(0, "Negras")
        self.assertFalse(self.tablero.puede_reingresar("Blancas", [1]))

    def test_todas_en_home(self):
        self.tablero.inicializar_piezas()
        # Mueve todas las blancas al home (posiciones 18-23)
        for pos in [0, 11, 16, 18]:
            while self.tablero.mostrar_tablero()[pos]:
                self.tablero.sacar_pieza(pos)
        for i in range(15):
            self.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.tablero._tablero__barra__ = {"Blancas": 0, "Negras": 0}
        self.assertTrue(self.tablero.todas_en_home("Blancas"))

    def test_sacar_ficha_fuera(self):
        self.tablero.inicializar_piezas()
        # Lleva todas las blancas al home
        for pos in [0, 11, 16, 18]:
            while self.tablero.mostrar_tablero()[pos]:
                self.tablero.sacar_pieza(pos)
        for i in range(15):
            self.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.tablero._tablero__barra__ = {"Blancas": 0, "Negras": 0}
        self.assertTrue(self.tablero.sacar_ficha_fuera("Blancas", 18))
        self.assertEqual(self.tablero.mostrar_tablero()[18].count("Blancas"), 4)

    def test_fichas_en_barra(self):
        self.tablero.inicializar_piezas()
        self.tablero._tablero__barra__["Blancas"] = 2
        self.assertEqual(self.tablero.fichas_en_barra("Blancas"), 2)

if __name__ == "__main__":
    unittest.main() 