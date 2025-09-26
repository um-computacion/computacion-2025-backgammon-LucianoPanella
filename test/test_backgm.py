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
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(1 <= d <= 6 for d in resultado))

    def test_cambiar_turno(self):
        jugador_inicial = self.game.turno_actual
        self.game.cambiar_turno()
        self.assertNotEqual(self.game.turno_actual, jugador_inicial)
        self.game.cambiar_turno()
        self.assertEqual(self.game.turno_actual, jugador_inicial)

    def test_mover_pieza_valido(self):
        self.game.tablero.inicializar_piezas()
        origen = 0  # Posición inicial de blancas
        destino = 1  # Siguiente posición (vacía al inicio)
        self.assertTrue(self.game.mover(origen, destino))
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[origen]), 1)
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[destino]), 1)

    def test_mover_pieza_invalido(self):
        self.assertFalse(self.game.mover(3, 4))

    def test_puede_reingresar(self):
        self.game.tablero.inicializar_piezas()
        # Simula una ficha blanca en la barra
        self.game.tablero._tablero__barra__["Blancas"] = 1
        self.game.dados_actuales = [1]
        self.assertTrue(self.game.puede_reingresar())

    def test_reingresar_desde_barra(self):
        self.game.tablero.inicializar_piezas()
        self.game.tablero._tablero__barra__["Blancas"] = 1
        destino = 1
        self.assertTrue(self.game.reingresar_desde_barra(destino))
        self.assertEqual(self.game.tablero.fichas_en_barra("Blancas"), 0)
        self.assertIn("Blancas", self.game.tablero.mostrar_tablero()[destino])

    def test_fichas_en_barra(self):
        self.game.tablero.inicializar_piezas()
        self.game.tablero._tablero__barra__["Blancas"] = 2
        self.assertEqual(self.game.fichas_en_barra("Blancas"), 2)

    def test_todas_en_home(self):
        self.game.tablero.inicializar_piezas()
        # Mueve todas las blancas al home (posiciones 18-23)
        for pos in [0, 11, 16, 18]:
            while self.game.tablero.mostrar_tablero()[pos]:
                self.game.tablero.sacar_pieza(pos)
        for i in range(15):
            self.game.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.game.tablero._tablero__barra__["Blancas"] = 0
        self.assertTrue(self.game.todas_en_home())

    def test_sacar_ficha_fuera(self):
        self.game.tablero.inicializar_piezas()
        # Lleva todas las blancas al home
        for pos in [0, 11, 16, 18]:
            while self.game.tablero.mostrar_tablero()[pos]:
                self.game.tablero.sacar_pieza(pos)
        for i in range(15):
            self.game.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.game.tablero._tablero__barra__["Blancas"] = 0
        self.assertTrue(self.game.sacar_ficha_fuera(18))
        self.assertEqual(self.game.tablero.mostrar_tablero()[18].count("Blancas"), 4)

    def test_juego_terminado_y_ganador(self):
        self.game.jugador1._jugador__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Lucia")
        self.game.jugador1._jugador__fichas_restantes__ = 1
        self.game.jugador2._jugador__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Juan")

    def test_estado_tablero(self):
        estado = self.game.estado_tablero()
        self.assertIsInstance(estado, list)
        self.assertEqual(len(estado), 24)

    def test_estado_jugador(self):
        estado = self.game.estado_jugador()
        self.assertIn("nombre", estado)
        self.assertIn("color", estado)
        self.assertIn("fichas_restantes", estado)
        self.assertIn("en_barra", estado)

if __name__ == "__main__":
    unittest.main()
#Revisar