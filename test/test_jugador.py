import unittest
from core.jugador import jugador

class TestJugador(unittest.TestCase):

    def test_init_blanco(self):
        jugador1 = jugador("Luciano", "blanco")
        self.assertEqual(jugador1.__nombre__, "Luciano")
        self.assertEqual(jugador1.__color__, "blanco")

    def test_init_negro(self):
        jugador2 = jugador("Ana", "negro")
        self.assertEqual(jugador2.__nombre__, "Ana")
        self.assertEqual(jugador2.__color__, "negro")

    def test_str_blanco(self):
        jugador1 = jugador("Luciano", "blanco")
        self.assertEqual(str(jugador1), "Jugador: Luciano, Color: blanco")

    def test_str_negro(self):
        jugador2 = jugador("Ana", "negro")
        self.assertEqual(str(jugador2), "Jugador: Ana, Color: negro")

    def test_jugadores_diferentes(self):
        jugador1 = jugador("Luciano", "blanco")
        jugador2 = jugador("Ana", "negro")
        self.assertNotEqual(jugador1.__color__, jugador2.__color__)
        self.assertNotEqual(jugador1.__nombre__, jugador2.__nombre__)

    def test_valores_vacios(self):
        jugador1 = jugador("", "")
        self.assertEqual(str(jugador1), "Jugador: , Color: ")

    def test_valores_nulos(self):
        jugador1 = jugador(None, None)
        self.assertEqual(str(jugador1), "Jugador: None, Color: None")

if __name__ == "__main__":
     unittest.main()
