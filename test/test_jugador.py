import unittest
from core.jugador import jugador
from core.excepciones import JugadorYaGano, FichaNoDisponible

class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = jugador("Lucia", "Blancas")

    def test_inicializacion(self):
        self.assertEqual(self.jugador.obtener_nombre(), "Lucia")
        self.assertEqual(self.jugador.obtener_color(), "Blancas")
        self.assertEqual(self.jugador.mostrar_fichas_restantes(), 15)

    def test_sacar_ficha_a_afuera(self):
        self.assertTrue(self.jugador.sacar_ficha_a_afuera())
        self.assertEqual(self.jugador.mostrar_fichas_restantes(), 14)
        # Sacar todas las fichas
        for _ in range(14):
            self.jugador.sacar_ficha_a_afuera()
        self.assertEqual(self.jugador.mostrar_fichas_restantes(), 0)
        # Intentar sacar cuando ya no quedan debe lanzar JugadorYaGano
        with self.assertRaises(JugadorYaGano):
            self.jugador.sacar_ficha_a_afuera()

    def test_gano(self):
        self.assertFalse(self.jugador.gano())
        for _ in range(15):
            self.jugador.sacar_ficha_a_afuera()
        self.assertTrue(self.jugador.gano())

    def test_str(self):
        texto = str(self.jugador)
        self.assertIn("Lucia", texto)
        self.assertIn("Blancas", texto)
        self.assertIn("Fichas restantes", texto)

if __name__ == "__main__":
    unittest.main()