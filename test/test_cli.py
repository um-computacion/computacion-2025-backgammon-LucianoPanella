"""
Referencia sobre mocking en tests de Python:
https://www.paradigmadigital.com/dev/mockear-tests-python/
"""

import io
import unittest
from unittest.mock import patch, MagicMock
from core.excepciones import BackgammonError, JuegoYaTerminado


class FakeJugador:
    def __init__(self, nombre, color):
        self._n = nombre
        self._c = color
    def obtener_nombre(self):
        return self._n
    def obtener_color(self):
        return self._c
    def mostrar_fichas_restantes(self):
        return 15


class FakeTablero:
    def __init__(self, piezas=None, puede_reingresar=False):
        # piezas: lista de 24 posiciones (listas), si None: un blanco en 0
        if piezas is None:
            self._t = [["Blancas"], *([[]] * 23)]
        else:
            self._t = piezas
        self._puede_reingresar = puede_reingresar

    def mostrar_tablero(self):
        return self._t

    def validar_movimiento(self, origen, destino, color):
        return True

    def puede_reingresar(self, color, dados):
        return self._puede_reingresar


class TestCLI(unittest.TestCase):

    @patch("cli.cli.Backgammon")
    def test_mover_origen_invalido_muestra_mensaje(self, MockBackgammon):
        from cli import cli as cli_module

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()  # hay al menos un movimiento posible
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [3, 4]
        fake.todas_en_home.return_value = False
        # Termina el juego después del primer bucle de turno
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        inputs = iter([
            "Jugador1",           # nombre1
            "Jugador2",           # nombre2
            "",                   # enter para tirar
            "1",                  # opción mover
            "27",                 # origen inválido (fuera de rango)
        ])

        with patch("builtins.input", side_effect=lambda *a, **k: next(inputs)) as _input, \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            # Forzamos un KeyboardInterrupt tras consumir los inputs
            _input.side_effect = ["Jugador1", "Jugador2", "", "1", "27", KeyboardInterrupt]
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Origen inválido", out)

    @patch("cli.cli.Backgammon")
    def test_opcion_invalida_muestra_mensaje(self, MockBackgammon):
        from cli import cli as cli_module

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [2, 3]
        fake.todas_en_home.return_value = False
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["J1", "J2", "", "9", KeyboardInterrupt]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Opción inválida", out)

    @patch("cli.cli.Backgammon")
    def test_no_hay_reingreso_posible_pierde_turno(self, MockBackgammon):
        from cli import cli as cli_module

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero(puede_reingresar=False)
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 1  # hay barra
        fake.tirar_dados.return_value = [6, 6]
        fake.todas_en_home.return_value = False
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["A", "B", "", KeyboardInterrupt]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("No hay reingresos posibles", out)

    @patch("cli.cli.Backgammon")
    def test_sin_movimientos_disponibles_pierde_turno(self, MockBackgammon):
        from cli import cli as cli_module

        # Tablero sin movimientos posibles: hacemos que validar_movimiento nunca sea alcanzable
        # devolviendo una grilla vacía (hay_movimiento_posible -> False)
        piezas_vacias = [[] for _ in range(24)]
        fake_tablero = FakeTablero(piezas=piezas_vacias)

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = fake_tablero
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [5, 6]
        fake.todas_en_home.return_value = False
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["A", "B", "", KeyboardInterrupt]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("No hay movimientos posibles", out)

    @patch("cli.cli.Backgammon")
    def test_nombres_vacios_requiere_reingreso(self, MockBackgammon):
        from cli import cli as cli_module

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [2, 3]
        fake.todas_en_home.return_value = False
        fake.juego_terminado.side_effect = [True]
        fake.obtener_ganador.return_value = None
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["", "J1", "", "J2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("El nombre no puede estar vacío.", out)

    @patch("cli.cli.Backgammon")
    def test_reingresar_con_entrada_invalida_y_luego_ok(self, MockBackgammon):
        from cli import cli as cli_module

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero(puede_reingresar=True)
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 1
        fake.tirar_dados.return_value = [4, 2]
        fake.todas_en_home.return_value = False
        fake.reingresar_desde_barra.return_value = True
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        # Secuencia: nombres, enter, destino invalido no-num -> error, luego destino 3 ok,
        # dado invalido no-num -> error, luego dado 4 ok
        inputs = [
            "A", "B", "",  # nombres y tirar
            "x", "3",        # destino invalido y luego valido
            "y", "4",        # dado invalido y luego valido
            KeyboardInterrupt,
        ]
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Debe reingresar una ficha desde la barra.", out)
        self.assertIn("Origen inválido", out) or self.assertIn("debe ser un número", out)

    @patch("cli.cli.Backgammon")
    def test_reingresar_destino_bloqueado_muestra_error(self, MockBackgammon):
        from cli import cli as cli_module
        from core.excepciones import DestinoBloqueado

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero(puede_reingresar=True)
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 1
        fake.tirar_dados.return_value = [3, 3]
        fake.todas_en_home.return_value = False
        fake.reingresar_desde_barra.side_effect = DestinoBloqueado("bloqueado")
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["A", "B", "", "2", "3", KeyboardInterrupt]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Error al reingresar", out)

    @patch("cli.cli.Backgammon")
    def test_mover_excepcion_movimiento_invalido(self, MockBackgammon):
        from cli import cli as cli_module
        from core.excepciones import MovimientoInvalido

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [2, 3]
        fake.todas_en_home.return_value = False
        fake.mover.side_effect = MovimientoInvalido("mov invalido")
        fake.juego_terminado.side_effect = [False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["A", "B", "", "1", "0", "2", KeyboardInterrupt]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Error en el movimiento", out)

    @patch("cli.cli.Backgammon")
    def test_sacar_ficha_en_home_exito_y_excepciones(self, MockBackgammon):
        from cli import cli as cli_module
        from core.excepciones import NoPuedeSacarFicha, FichaNoDisponible, JugadorYaGano

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        fake.tirar_dados.return_value = [1, 1]
        # Simular primero en_home True para mostrar opción 2
        fake.todas_en_home.side_effect = [True, True, True, True]
        # Éxito al sacar, luego distintas excepciones en siguientes intentos
        fake.sacar_ficha_fuera.side_effect = [True, NoPuedeSacarFicha("no home"), FichaNoDisponible("sd"), JugadorYaGano("jg")]
        fake.juego_terminado.side_effect = [False, False, False, False, True]
        MockBackgammon.return_value = fake

        # Flujo: nombres, enter, opcion 2, origen 18, dado 1
        # Luego repetir para disparar excepciones
        with patch("builtins.input", side_effect=[
            "A", "B", "", "2", "18", "1",
            "2", "18", "1",
            "2", "18", "1",
            "2", "18", "1",
            KeyboardInterrupt
        ]), patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            try:
                cli_module.main()
            except KeyboardInterrupt:
                pass
            out = fake_out.getvalue()

        self.assertIn("Ficha sacada del tablero.", out)
        self.assertIn("Error al sacar ficha", out)

    @patch("cli.cli.Backgammon")
    def test_dados_no_tirados_y_cambiar_turno_error(self, MockBackgammon):
        from cli import cli as cli_module
        from core.excepciones import DadosNoTirados, TurnoIncorrecto

        fake = MagicMock()
        fake.turno_actual = FakeJugador("J1", "Blancas")
        fake.tablero = FakeTablero()
        fake.estado_tablero_visual.return_value = "TABLERO"
        fake.fichas_en_barra.return_value = 0
        # Primera vez tira: DadosNoTirados, segunda vez: devuelve dados [1,1]
        fake.tirar_dados.side_effect = [DadosNoTirados("no tirados"), [1, 1]]
        fake.todas_en_home.return_value = False
        # Consumimos dados con opción 1 inválida para no mover realmente y terminar el loop
        fake.mover.return_value = False
        # Al cambiar turno, lanzar TurnoIncorrecto
        fake.cambiar_turno.side_effect = TurnoIncorrecto("no turno")
        # Loop: no termina inmediatamente
        fake.juego_terminado.side_effect = [False, False, False, True]
        MockBackgammon.return_value = fake

        with patch("builtins.input", side_effect=["A", "B", "", "", "1", "0", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("Error con los dados", out)
        self.assertIn("Error al cambiar turno", out)

    

    @patch("cli.cli.Backgammon")
    def test_tirar_dados_juego_ya_terminado(self, MockBackgammon):
        from cli import cli as cli_module

        juego = MagicMock()
        juego.turno_actual.obtener_nombre.return_value = "J1"
        juego.turno_actual.obtener_color.return_value = "Blancas"
        juego.estado_tablero_visual.return_value = "TABLERO"
        juego.fichas_en_barra.return_value = 0
        juego.tirar_dados.side_effect = JuegoYaTerminado("fin")
        juego.juego_terminado.side_effect = [False]
        juego.obtener_ganador.return_value = None
        MockBackgammon.return_value = juego

        with patch("builtins.input", side_effect=["A", "B", ""]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("Error:", out)
        self.assertIn("¡Juego terminado!", out)
        self.assertIn("No hay ganador.", out)

    @patch("cli.cli.Backgammon")
    def test_error_del_juego_y_usuario_elije_salir(self, MockBackgammon):
        from cli import cli as cli_module

        juego = MagicMock()
        juego.turno_actual.obtener_nombre.return_value = "J1"
        juego.turno_actual.obtener_color.return_value = "Blancas"
        juego.estado_tablero_visual.return_value = "TABLERO"
        juego.fichas_en_barra.return_value = 0
        juego.tirar_dados.side_effect = BackgammonError("fallo")
        juego.juego_terminado.side_effect = [False]
        MockBackgammon.return_value = juego

        with patch("builtins.input", side_effect=["A", "B", "", "n"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("Error del juego:", out)
        self.assertIn("¡Juego terminado!", out)

    @patch("cli.cli.Backgammon")
    def test_error_al_finalizar_el_juego(self, MockBackgammon):
        from cli import cli as cli_module

        juego = MagicMock()
        juego.juego_terminado.return_value = True
        juego.obtener_ganador.side_effect = Exception("fin error")
        MockBackgammon.return_value = juego

        with patch("builtins.input", side_effect=["A", "B"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("¡Juego terminado!", out)
        self.assertIn("Error al finalizar el juego:", out)

    @patch("cli.cli.Backgammon", side_effect=Exception("boom init"))
    def test_error_al_inicializar(self, MockBackgammon):
        from cli import cli as cli_module

        with patch("builtins.input", side_effect=["A", "B"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("Error al inicializar el juego:", out)

    @patch("cli.cli.Backgammon")
    def test_mensaje_ganador(self, MockBackgammon):
        from cli import cli as cli_module

        juego = MagicMock()
        juego.juego_terminado.return_value = True
        juego.obtener_ganador.return_value = "Jugador1"
        MockBackgammon.return_value = juego

        with patch("builtins.input", side_effect=["A", "B"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            cli_module.main()
            out = fake_out.getvalue()

        self.assertIn("¡Juego terminado!", out)
        self.assertIn("Felicidades Jugador1", out)


if __name__ == "__main__":
	unittest.main()
