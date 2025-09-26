import unittest
from core.jugador import jugador

class TestJugador(unittest.TestCase):

    def setUp(self):
        self.j = jugador("Lucia", "Blancas")

    def test_inicializacion(self):
        self.assertEqual(self.j.obtener_nombre(), "Lucia")
        self.assertEqual(self.j.obtener_color(), "Blancas")
        self.assertEqual(self.j.mostrar_fichas_restantes(), 15)
        self.assertFalse(self.j.tiene_en_barra())

    def test_sacar_ficha_a_afuera(self):
        self.assertTrue(self.j.sacar_ficha_a_afuera())
        self.assertEqual(self.j.mostrar_fichas_restantes(), 14)

    def test_no_puede_sacar_mas_fichas(self):
        # Saca todas las fichas
        for _ in range(15):
            self.j.sacar_ficha_a_afuera()
        self.assertEqual(self.j.mostrar_fichas_restantes(), 0)
        self.assertFalse(self.j.sacar_ficha_a_afuera())

    def test_gano(self):
        for _ in range(15):
            self.j.sacar_ficha_a_afuera()
        self.assertTrue(self.j.gano())

    def test_agregar_y_quitar_barra(self):
        self.j.agregar_a_barra()
        self.assertTrue(self.j.tiene_en_barra())
        self.assertTrue(self.j.quitar_de_barra())
        self.assertFalse(self.j.tiene_en_barra())

    def test_quitar_de_barra_sin_fichas(self):
        self.assertFalse(self.j.quitar_de_barra())

    def test_str(self):
        texto = str(self.j)
        self.assertIn("Jugador: Lucia", texto)
        self.assertIn("Color: Blancas", texto)
        self.assertIn("Fichas restantes: 15", texto)
        self.assertIn("En barra: 0", texto)

if __name__ == "__main__":
    unittest.main()