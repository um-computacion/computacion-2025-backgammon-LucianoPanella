import unittest
from core.backgammon import Backgammon

class TestBackgammon(unittest.TestCase):

    def setUp(self):
        self.game = Backgammon("Lucia", "Blancas", "Juan", "Negras")

    def test_inicializacion(self):
        self.assertEqual(self.game.jugador1.obtener_nombre(), "Lucia")
        self.assertEqual(self.game.jugador2.obtener_nombre(), "Juan")
        self.assertEqual(self.game.jugador1.obtener_color(), "Blancas")
        self.assertEqual(self.game.jugador2.obtener_color(), "Negras")
        self.assertEqual(len(self.game.tablero.mostrar_tablero()), 24)

    def test_tirar_dados(self):
        resultado = self.game.tirar_dados()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(1 <= d <= 6 for d in resultado))

    def test_cambiar_turno(self):
        jugador_inicial = self.game.turno_actual
        self.game.cambiar_turno()
        self.assertNotEqual(self.game.turno_actual, jugador_inicial)
        self.game.cambiar_turno()
        self.assertEqual(self.game.turno_actual, jugador_inicial)

    def test_mover_pieza_valido(self):
        # Busca una posición inicial válida para mover una ficha blanca
        self.game.tablero.inicializar_piezas()
        origen = 0  # Posición inicial de blancas
        destino = 1  # Siguiente posición (vacía al inicio)
        self.assertTrue(self.game.mover(origen, destino))
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[origen]), 1)
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[destino]), 1)

    def test_mover_pieza_invalido(self):
        # Intenta mover desde una posición vacía
        self.assertFalse(self.game.mover(3, 4))

    def test_juego_terminado_y_ganador(self):
        # Simula que jugador1 saca todas sus fichas
        self.game.jugador1._jugador__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Lucia")

        # Simula que jugador2 saca todas sus fichas
        self.game.jugador1._jugador__fichas_restantes__ = 1
        self.game.jugador2._jugador__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Juan")

if __name__ == "__main__":
    unittest.main()