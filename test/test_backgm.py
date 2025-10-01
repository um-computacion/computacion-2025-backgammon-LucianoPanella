import unittest
from core.backgammon import Backgammon
from core.excepciones import TurnoIncorrecto, JuegoYaTerminado

class TestBackgammon(unittest.TestCase):

    def setUp(self):
        self.game = Backgammon("Lucia", "Blancas", "Juan", "Negras")

    def test_inicializacion(self):
        # Verifica la inicialización correcta del juego
        self.assertEqual(self.game.jugador1.obtener_nombre(), "Lucia")
        self.assertEqual(self.game.jugador2.obtener_nombre(), "Juan")
        self.assertEqual(self.game.jugador1.obtener_color(), "Blancas")
        self.assertEqual(self.game.jugador2.obtener_color(), "Negras")
        self.assertEqual(len(self.game.tablero.mostrar_tablero()), 24)

    def test_tirar_dados(self):
        # Verifica que tirar dados funciona correctamente
        resultado = self.game.tirar_dados()
        self.assertIsInstance(resultado, list)
        self.assertTrue(2 <= len(resultado) <= 4)
        self.assertTrue(all(1 <= d <= 6 for d in resultado))

    def test_tirar_dados_juego_terminado(self):
        # Verifica excepción al tirar dados con juego terminado - Línea 29
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.tirar_dados()

    def test_cambiar_turno(self):
        # Verifica cambio de turno básico
        jugador_inicial = self.game.turno_actual
        self.game.cambiar_turno()
        self.assertNotEqual(self.game.turno_actual, jugador_inicial)
        self.game.cambiar_turno()
        self.assertEqual(self.game.turno_actual, jugador_inicial)

    def test_cambiar_turno_juego_terminado(self):
        # Verifica excepción al cambiar turno con juego terminado - Línea 39
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.cambiar_turno()

    def test_mover_pieza_valido(self):
        # Verifica movimiento válido
        self.game.tablero.inicializar_piezas()
        origen = 0  # Posición inicial de blancas
        destino = 1  # Siguiente posición (vacía al inicio)
        self.assertTrue(self.game.mover(origen, destino))
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[origen]), 1)
        self.assertEqual(len(self.game.tablero.mostrar_tablero()[destino]), 1)

    def test_mover_pieza_invalido(self):
        # Verifica movimiento inválido devuelve False
        self.assertFalse(self.game.mover(3, 4))

    def test_mover_juego_terminado(self):
        # Verifica excepción al mover con juego terminado - Línea 55
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.mover(0, 1)

    def test_puede_reingresar(self):
        # Verifica si puede reingresar fichas desde la barra
        self.game.tablero.inicializar_piezas()
        # Simula una ficha blanca en la barra
        self.game.tablero.__barra__["Blancas"] = 1
        self.game.dados_actuales = [1]
        self.assertTrue(self.game.puede_reingresar())

    def test_puede_reingresar_juego_terminado(self):
        # Verifica excepción al verificar reingreso con juego terminado - Línea 63
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.puede_reingresar()

    def test_reingresar_desde_barra(self):
        # Verifica reingreso exitoso desde la barra
        self.game.tablero.inicializar_piezas()
        self.game.tablero.__barra__["Blancas"] = 1
        destino = 1
        self.assertTrue(self.game.reingresar_desde_barra(destino))
        self.assertEqual(self.game.tablero.fichas_en_barra("Blancas"), 0)
        self.assertIn("Blancas", self.game.tablero.mostrar_tablero()[destino])

    def test_reingresar_desde_barra_juego_terminado(self):
        # Verifica excepción al reingresar con juego terminado - Línea 70
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.reingresar_desde_barra(1)

    def test_reingresar_desde_barra_verifica_fin_juego(self):
        # Verifica que se llama _verificar_fin_juego después de reingresar - Línea 81
        self.game.tablero.inicializar_piezas()
        self.game.tablero.__barra__["Blancas"] = 1
        # Simular que el jugador está a punto de ganar
        self.game.jugador1.__fichas_restantes__ = 1
        original_verificar = self.game._verificar_fin_juego
        verificar_llamado = False
        def mock_verificar():
            nonlocal verificar_llamado
            verificar_llamado = True
            original_verificar()
        self.game._verificar_fin_juego = mock_verificar
        self.game.reingresar_desde_barra(1)
        self.assertTrue(verificar_llamado)

    def test_fichas_en_barra(self):
        # Verifica conteo de fichas en barra
        self.game.tablero.inicializar_piezas()
        self.game.tablero.__barra__["Blancas"] = 2
        self.assertEqual(self.game.fichas_en_barra("Blancas"), 2)

    def test_fichas_en_barra_sin_color(self):
        # Verifica fichas en barra del jugador actual sin especificar color
        self.game.tablero.__barra__["Blancas"] = 3
        self.assertEqual(self.game.fichas_en_barra(), 3)

    def test_todas_en_home(self):
        # Verifica que todas las fichas están en home
        self.game.tablero.inicializar_piezas()
        # Mueve todas las blancas al home (posiciones 18-23)
        for pos in [0, 11, 16, 18]:
            while self.game.tablero.mostrar_tablero()[pos]:
                self.game.tablero.sacar_pieza(pos)
        for i in range(15):
            self.game.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.game.tablero.__barra__["Blancas"] = 0
        self.assertTrue(self.game.todas_en_home())

    def test_sacar_ficha_fuera(self):
        # Verifica sacar ficha exitosamente
        self.game.tablero.inicializar_piezas()
        # Lleva todas las blancas al home
        for pos in [0, 11, 16, 18]:
            while self.game.tablero.mostrar_tablero()[pos]:
                self.game.tablero.sacar_pieza(pos)
        for i in range(15):
            self.game.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.game.tablero.__barra__["Blancas"] = 0
        cantidad_inicial = self.game.tablero.mostrar_tablero()[18].count("Blancas")
        self.assertTrue(self.game.sacar_ficha_fuera(18))
        self.assertEqual(self.game.tablero.mostrar_tablero()[18].count("Blancas"), cantidad_inicial - 1)

    def test_sacar_ficha_fuera_juego_terminado(self):
        # Verifica excepción al sacar ficha con juego terminado - Línea 94
        self.game._juego_terminado = True
        with self.assertRaises(JuegoYaTerminado):
            self.game.sacar_ficha_fuera(18)

    def test_sacar_ficha_fuera_invalido(self):
        # Verifica que devuelve False cuando no se puede sacar - Línea 110
        self.game.tablero.inicializar_piezas()
        # No todas están en home, no se puede sacar
        self.assertFalse(self.game.sacar_ficha_fuera(18))

    def test_verificar_fin_juego_jugador1_gana(self):
        # Verifica detección de fin de juego cuando jugador1 gana - Línea 119
        self.game.jugador1.__fichas_restantes__ = 0
        self.game._verificar_fin_juego()
        self.assertTrue(self.game._juego_terminado)

    def test_verificar_fin_juego_jugador2_gana(self):
        # Verifica detección de fin de juego cuando jugador2 gana - Línea 119
        self.game.jugador2.__fichas_restantes__ = 0
        self.game._verificar_fin_juego()
        self.assertTrue(self.game._juego_terminado)

    def test_juego_terminado_y_ganador(self):
        # Verifica detección correcta del ganador
        self.game.jugador1.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Lucia")
        self.game.jugador1.__fichas_restantes__ = 1
        self.game.jugador2.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), "Juan")

    def test_juego_terminado_con_flag_interno(self):
        # Verifica que juego_terminado detecta el flag interno - Línea 126
        self.game._juego_terminado = True
        self.assertTrue(self.game.juego_terminado())

    def test_obtener_ganador_sin_ganador(self):
        # Verifica que devuelve None cuando no hay ganador - Línea 142
        self.game.jugador1.__fichas_restantes__ = 5
        self.game.jugador2.__fichas_restantes__ = 7
        self.assertIsNone(self.game.obtener_ganador())

    def test_estado_tablero(self):
        # Verifica que devuelve el estado del tablero
        estado = self.game.estado_tablero()
        self.assertIsInstance(estado, list)
        self.assertEqual(len(estado), 24)

    def test_estado_tablero_visual(self):
        # Verifica que devuelve el estado visual del tablero - Línea 154
        estado_visual = self.game.estado_tablero_visual()
        self.assertIsInstance(estado_visual, str)
        self.assertIn("BAR", estado_visual)
        self.assertIn("HOME", estado_visual)

    def test_estado_jugador(self):
        # Verifica información del jugador actual
        estado = self.game.estado_jugador()
        self.assertIn("nombre", estado)
        self.assertIn("color", estado)
        self.assertIn("fichas_restantes", estado)
        self.assertIn("en_barra", estado)

    def test_estado_jugador_con_parametro(self):
        # Verifica información de jugador específico
        estado = self.game.estado_jugador(self.game.jugador2)
        self.assertEqual(estado["nombre"], "Juan")
        self.assertEqual(estado["color"], "Negras")

    def test_validar_turno_jugador_correcto(self):
        # Verifica validación exitosa del turno - Líneas 173-176
        self.assertTrue(self.game.validar_turno_jugador(self.game.jugador1))

    def test_validar_turno_jugador_incorrecto(self):
        # Verifica excepción con turno incorrecto - Líneas 173-176
        with self.assertRaises(TurnoIncorrecto) as context:
            self.game.validar_turno_jugador(self.game.jugador2)
        self.assertIn("No es el turno de Juan", str(context.exception))
        self.assertIn("Es el turno de Lucia", str(context.exception))

    def test_sacar_ficha_fuera_con_verificacion_fin_juego(self):
        # Verifica que sacar ficha llama a verificar fin de juego
        self.game.tablero.inicializar_piezas()
        # Prepara condiciones para sacar ficha
        for pos in [0, 11, 16, 18]:
            while self.game.tablero.mostrar_tablero()[pos]:
                self.game.tablero.sacar_pieza(pos)
        for i in range(15):
            self.game.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.game.tablero.__barra__["Blancas"] = 0
        
        # Simular que queda 1 ficha por sacar
        self.game.jugador1.__fichas_restantes__ = 1
        original_verificar = self.game._verificar_fin_juego
        verificar_llamado = False
        def mock_verificar():
            nonlocal verificar_llamado
            verificar_llamado = True
            original_verificar()
        self.game._verificar_fin_juego = mock_verificar
        
        self.game.sacar_ficha_fuera(18)
        self.assertTrue(verificar_llamado)

    def test_mover_con_verificacion_fin_juego(self):
        # Verifica que mover llama a verificar fin de juego
        self.game.tablero.inicializar_piezas()
        original_verificar = self.game._verificar_fin_juego
        verificar_llamado = False
        def mock_verificar():
            nonlocal verificar_llamado
            verificar_llamado = True
            original_verificar()
        self.game._verificar_fin_juego = mock_verificar
        
        self.game.mover(0, 1)
        self.assertTrue(verificar_llamado)

if __name__ == "__main__":
    unittest.main()