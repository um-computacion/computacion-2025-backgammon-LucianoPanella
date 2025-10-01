import unittest
from core.tablero import tablero
from core.dice import dice
from core.excepciones import DadosNoTirados, DadoNoDisponible
import random

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
        self.assertEqual(self.tablero.fichas_en_barra("Negras"), 1)

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
        self.tablero.__barra__["Blancas"] = 1
        destino = 1
        self.assertTrue(self.tablero.reingresar_desde_barra("Blancas", destino))
        self.assertEqual(self.tablero.fichas_en_barra("Blancas"), 0)
        self.assertIn("Blancas", self.tablero.mostrar_tablero()[destino])

    def test_no_reingresa_si_barra_vacia(self):
        self.tablero.inicializar_piezas()
        self.tablero.__barra__["Blancas"] = 0
        self.assertFalse(self.tablero.reingresar_desde_barra("Blancas", 1))

    def test_puede_reingresar(self):
        self.tablero.inicializar_piezas()
        self.tablero.__barra__["Blancas"] = 1
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
        self.tablero.__barra__["Blancas"] = 0
        self.assertTrue(self.tablero.todas_en_home("Blancas"))

    def test_sacar_ficha_fuera(self):
        self.tablero.inicializar_piezas()
        # Lleva todas las blancas al home (posiciones 18-23)
        for pos in [0, 11, 16, 18]:
            while self.tablero.mostrar_tablero()[pos]:
                self.tablero.sacar_pieza(pos)
        for i in range(15):
            self.tablero.colocar_pieza(18 + (i % 6), "Blancas")
        self.tablero.__barra__["Blancas"] = 0
        cantidad_inicial = self.tablero.mostrar_tablero()[18].count("Blancas")
        self.assertTrue(self.tablero.sacar_ficha_fuera("Blancas", 18))
        self.assertEqual(self.tablero.mostrar_tablero()[18].count("Blancas"), cantidad_inicial - 1)

    def test_fichas_en_barra(self):
        self.tablero.inicializar_piezas()
        self.tablero.__barra__["Blancas"] = 2
        self.assertEqual(self.tablero.fichas_en_barra("Blancas"), 2)

class TestDice(unittest.TestCase):

    def test_tirar_devuelve_lista(self):
        # Verifica que el método tirar devuelve una lista
        dado = dice()
        resultado = dado.tirar()
        self.assertIsInstance(resultado, list, "El resultado debe ser una lista.")

    def test_valores_entre_1_y_6(self):
        # Verifica que todos los valores están en el rango válido de dados
        dado = dice()
        resultado = dado.tirar()
        for valor in resultado:
            self.assertTrue(1 <= valor <= 6, f"El valor {valor} no está entre 1 y 6.")

    def test_tirada_doble(self):
        # Verifica que cuando salen valores iguales, se devuelven 4 elementos
        dado = dice()
        original_randint = random.randint
        random.randint = lambda a, b: 4
        resultado = dado.tirar()
        self.assertEqual(len(resultado), 4, "La tirada doble debe tener 4 valores.")
        self.assertTrue(all(v == 4 for v in resultado), "Todos los valores deben ser iguales en una tirada doble.")
        random.randint = original_randint

    def test_tirada_normal(self):
        # Verifica que cuando salen valores diferentes, se devuelven 2 elementos
        dado = dice()
        original_randint = random.randint
        valores = [2, 5]
        random.randint = lambda a, b: valores.pop(0)
        resultado = dado.tirar()
        self.assertEqual(len(resultado), 2, "Una tirada normal debe tener 2 valores.")
        self.assertEqual(resultado, [2, 5])
        random.randint = original_randint

    def test_obtener_ult_tirada_devuelve_ultima_tirada(self):
        # Verifica que obtener_ult_tirada devuelve la última tirada realizada
        dado = dice()
        resultado = dado.tirar()
        self.assertEqual(dado.obtener_ult_tirada(), resultado, "obtener_ult_tirada debe devolver la última tirada.")

    def test_ha_tirado_es_falso_al_inicio(self):
        # Verifica el estado inicial de _ha_tirado
        dado = dice()
        self.assertFalse(dado._ha_tirado, "Al inicio no debería haber tiradas.")

    def test_ha_tirado_es_verdadero_despues_de_tirar(self):
        # Verifica que _ha_tirado cambia a True después de tirar
        dado = dice()
        dado.tirar()
        self.assertTrue(dado._ha_tirado, "Después de tirar debería ser True.")

    def test_tirada_sin_haber_tirado_antes(self):
        # Verifica el comportamiento de tirada() cuando no se ha tirado antes
        dado = dice()
        # No ha tirado aún, debería llamar a tirar()
        resultado = dado.tirada()
        self.assertIsInstance(resultado, list)
        self.assertTrue(dado._ha_tirado)
        # Verificar que devuelve la tirada
        self.assertEqual(len(resultado), 2 or len(resultado) == 4)

    def test_tirada_despues_de_haber_tirado(self):
        # Verifica el comportamiento de tirada() cuando ya se ha tirado
        dado = dice()
        dado.tirar()  # Primera tirada
        resultado = dado.tirada()  # Segunda llamada
        # Debería devolver True porque ya se tiró
        self.assertTrue(resultado)

    def test_obtener_ult_tirada_sin_tirar(self):
        # Verifica que se lance excepción al obtener tirada sin haber tirado
        dado = dice()
        with self.assertRaises(DadosNoTirados) as context:
            dado.obtener_ult_tirada()
        self.assertIn("No se han tirado los dados aún", str(context.exception))

    def test_validar_dado_disponible_valido(self):
        # Verifica validación de dado disponible con valor válido
        dado = dice()
        dados_disponibles = [1, 2, 3, 4]
        resultado = dado.validar_dado_disponible(2, dados_disponibles)
        self.assertTrue(resultado)

    def test_validar_dado_disponible_invalido(self):
        # Verifica que se lance excepción con dado no disponible
        dado = dice()
        dados_disponibles = [1, 2, 3, 4]
        with self.assertRaises(DadoNoDisponible) as context:
            dado.validar_dado_disponible(5, dados_disponibles)
        self.assertIn("El dado 5 no está disponible", str(context.exception))
        self.assertIn("Dados disponibles: [1, 2, 3, 4]", str(context.exception))

    def test_reiniciar_turno(self):
        # Verifica que reiniciar_turno resetea el estado de los dados
        dado = dice()
        # Tirar dados primero
        dado.tirar()
        self.assertTrue(dado._ha_tirado)
        self.assertTrue(len(dado._ultima_tirada) > 0)
        
        # Reiniciar turno
        dado.reiniciar_turno()
        self.assertFalse(dado._ha_tirado)
        self.assertEqual(dado._ultima_tirada, [])

    def test_multiples_tiradas_dobles(self):
        # Verifica múltiples tipos de dobles
        dado = dice()
        original_randint = random.randint
        
        # Simular doble de 6
        random.randint = lambda a, b: 6
        resultado = dado.tirar()
        self.assertEqual(resultado, [6, 6, 6, 6])
        
        # Reiniciar y probar doble de 1
        dado.reiniciar_turno()
        random.randint = lambda a, b: 1
        resultado = dado.tirar()
        self.assertEqual(resultado, [1, 1, 1, 1])
        
        random.randint = original_randint

    def test_validar_dado_disponible_lista_vacia(self):
        # Verifica comportamiento con lista vacía de dados disponibles
        dado = dice()
        with self.assertRaises(DadoNoDisponible):
            dado.validar_dado_disponible(1, [])

    def test_validar_dado_disponible_con_duplicados(self):
        # Verifica validación con dados duplicados (como en dobles)
        dado = dice()
        dados_disponibles = [2, 2, 2, 2]  # Como en un doble
        resultado = dado.validar_dado_disponible(2, dados_disponibles)
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()