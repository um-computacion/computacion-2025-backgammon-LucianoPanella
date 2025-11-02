#FINALIZADO#
from core.backgammon import Backgammon
from core.constants import BLANCAS, NEGRAS, BOARD_POINTS
from core.excepciones import (
    BackgammonError, MovimientoInvalido, PosicionFueraDeRango, 
    OrigenSinFicha, DestinoBloqueado, NoPuedeReingresar, 
    NoPuedeSacarFicha, FichaNoDisponible, JugadorYaGano,
    DadosNoTirados, DadoNoDisponible, TurnoIncorrecto, 
    JuegoYaTerminado,
    EntradaInvalida, OpcionInvalida, DebeReingresarPrimero,
    NoHayReingresoPosible, SinMovimientosDisponibles,
)

def mostrar_tablero(juego):
    # Muestra el estado actual del tablero en formato visual de Backgammon
    print(juego.estado_tablero_visual())

def hay_movimiento_posible(juego, dados_disponibles):
    """
    Devuelve True si existe al menos un movimiento legal en el tablero
    para el jugador actual con alguno de los dados disponibles.
    No contempla reingreso desde barra (se maneja aparte) ni las reglas finas de bearing off por dado.
    """
    color = juego.turno_actual.obtener_color()
    t = juego.tablero
    tablero_actual = t.mostrar_tablero()
    for origen, pila in enumerate(tablero_actual):
        if pila and pila[-1] == color:
            for d in dados_disponibles:
                destino = origen + d if color == BLANCAS else origen - d
                if 0 <= destino < BOARD_POINTS:
                    try:
                        t.validar_movimiento(origen, destino, color)
                        return True
                    except Exception:
                        pass
    return False

def puede_reingresar_con(juego, dados_disponibles):
    color = juego.turno_actual.obtener_color()
    return juego.tablero.puede_reingresar(color, dados_disponibles)

def main():
    print("Bienvenido a Backgammon (CLI)\n")
    
    try:
        # Solicita los nombres de los jugadores
        while True:
            nombre1 = input(f"Ingrese el nombre del Jugador 1 ({BLANCAS}): ").strip()
            if nombre1:
                break
            print("El nombre no puede estar vacío.")
        while True:
            nombre2 = input(f"Ingrese el nombre del Jugador 2 ({NEGRAS}): ").strip()
            if nombre2:
                break
            print("El nombre no puede estar vacío.")

        # Inicializa el juego con los nombres y colores
        juego = Backgammon(nombre1, BLANCAS, nombre2, NEGRAS)

        # Bucle principal del juego
        while not juego.juego_terminado():
            try:
                jugador = juego.turno_actual
                print(f"\nTurno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
                mostrar_tablero(juego)  # CAMBIO: pasamos el objeto juego completo
                print(f"Fichas restantes: {jugador.mostrar_fichas_restantes()}")
                print(f"Fichas en barra: {juego.fichas_en_barra()}")

                # El jugador tira los dados al inicio de su turno
                input(f"{jugador.obtener_nombre()}, presione Enter para tirar los dados...")
                
                try:
                    dados = juego.tirar_dados()
                    print(f"Dados disponibles: {dados}")
                except JuegoYaTerminado as e:
                    print(f"Error: {getattr(e, 'message', str(e))}")
                    break
                except DadosNoTirados as e:
                    print(f"Error con los dados: {getattr(e, 'message', str(e))}")
                    continue

                # Copia los dados para ir eliminando los usados
                dados_disponibles = dados.copy()

                # Mientras queden dados por usar, el jugador DEBE realizar movimientos
                while dados_disponibles:
                    try:
                        mostrar_tablero(juego)
                        print(f"\nTurno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
                        print(f"Dados restantes: {dados_disponibles}")

                        # Si hay fichas en la barra, está obligado a reingresar
                        if juego.fichas_en_barra() > 0:
                            if not puede_reingresar_con(juego, dados_disponibles):
                                raise NoHayReingresoPosible("No hay reingresos posibles con los dados actuales. Pierdes el turno.")
                            try:
                                print("Debe reingresar una ficha desde la barra.")
                                # Elegir destino válido
                                while True:
                                    try:
                                        destino = int(input("Ingrese la posición de destino para reingresar: "))
                                        if 0 <= destino < BOARD_POINTS:
                                            break
                                        print(f"La posición debe estar entre 0 y {BOARD_POINTS-1}.")
                                    except (ValueError, TypeError):
                                        print("Origen inválido: debe ser un número.")
                                # Elegir dado a usar
                                print(f"Dados disponibles para reingresar: {dados_disponibles}")
                                while True:
                                    try:
                                        dado_usado = int(input("¿Qué dado desea usar para reingresar? "))
                                        break
                                    except (ValueError, TypeError):
                                        print("Origen inválido: debe ser un número.")

                                if dado_usado in dados_disponibles:
                                    if juego.reingresar_desde_barra(destino):
                                        print("Ficha reingresada correctamente.")
                                        dados_disponibles.remove(dado_usado)
                                    else:
                                        print("No se pudo reingresar la ficha. Intente otra posición.")
                                else:
                                    print("Dado no válido.")
                            except (PosicionFueraDeRango, NoPuedeReingresar, DestinoBloqueado) as e:
                                print(f"Error al reingresar: {getattr(e, 'message', str(e))}")
                            except (ValueError, TypeError):
                                print("Error: Por favor ingrese números válidos.")
                            except JuegoYaTerminado as e:
                                print(f"Error: {getattr(e, 'message', str(e))}")
                                break
                            continue

                        # Si no hay barra: sólo mover; opcionalmente "sacar" si todas en home
                        en_home = juego.todas_en_home()
                        # Si no hay ningún movimiento posible con los dados restantes, pierde el turno
                        if not hay_movimiento_posible(juego, dados_disponibles) and not en_home:
                            raise SinMovimientosDisponibles("No hay movimientos posibles con los dados actuales. Pierdes el turno.")

                        # Menú dinámico
                        print("Opciones: ")
                        print("1. Mover ficha")
                        if en_home:
                            print("2. Sacar ficha fuera del tablero")

                        opcion = input("Seleccione una opción: ")

                        if opcion == "1":
                            # Mover ficha usando un dado específico
                            try:
                                # Ingreso de origen validado con excepción explícita
                                try:
                                    origen_str = input("Origen: ")
                                    origen = int(origen_str)
                                    if not (0 <= origen < BOARD_POINTS):
                                        raise EntradaInvalida(f"Origen inválido: debe ser un número entre 0 y {BOARD_POINTS-1}.")
                                except (ValueError, TypeError):
                                    raise EntradaInvalida("Origen inválido: debe ser un número.")
                                print(f"Dados disponibles para mover: {dados_disponibles}")
                                try:
                                    dado_str = input("¿Qué dado desea usar para mover? ")
                                    dado_usado = int(dado_str)
                                except (ValueError, TypeError):
                                    raise EntradaInvalida("Dado inválido: debe ser un número.")

                                if dado_usado in dados_disponibles:
                                    color = jugador.obtener_color()
                                    destino = origen + dado_usado if color == BLANCAS else origen - dado_usado
                                    if 0 <= destino < BOARD_POINTS and juego.mover(origen, destino):
                                        print(f"Movimiento realizado de {origen} a {destino} usando dado {dado_usado}.")
                                        dados_disponibles.remove(dado_usado)
                                    else:
                                        print("Movimiento inválido.")
                                    mostrar_tablero(juego)
                                else:
                                    print("Dado no válido.")

                            except (MovimientoInvalido, PosicionFueraDeRango, OrigenSinFicha, DestinoBloqueado) as e:
                                print(f"Error en el movimiento: {getattr(e, 'message', str(e))}")
                            except (ValueError, TypeError):
                                print("Error: Por favor ingrese números válidos.")
                            except JuegoYaTerminado as e:
                                print(f"Error: {getattr(e, 'message', str(e))}")
                                break

                        elif opcion == "2" and en_home:
                            # Sacar ficha fuera del tablero usando un dado específico (solo si todas en home)
                            try:
                                try:
                                    origen_str = input("Origen de la ficha a sacar: ")
                                    origen = int(origen_str)
                                    if not (0 <= origen < BOARD_POINTS):
                                        raise EntradaInvalida(f"Origen inválido: debe ser un número entre 0 y {BOARD_POINTS-1}.")
                                except (ValueError, TypeError):
                                    raise EntradaInvalida("Origen inválido: debe ser un número.")
                                print(f"Dados disponibles para sacar ficha: {dados_disponibles}")
                                try:
                                    dado_str = input("¿Qué dado desea usar para sacar ficha? ")
                                    dado_usado = int(dado_str)
                                except (ValueError, TypeError):
                                    raise EntradaInvalida("Dado inválido: debe ser un número.")

                                if dado_usado in dados_disponibles:
                                    if juego.sacar_ficha_fuera(origen):
                                        print("Ficha sacada del tablero.")
                                        dados_disponibles.remove(dado_usado)
                                    else:
                                        print("No se pudo sacar la ficha. Verifique que todas estén en el home.")
                                    mostrar_tablero(juego)
                                else:
                                    print("Dado no válido.")

                            except (NoPuedeSacarFicha, PosicionFueraDeRango, OrigenSinFicha, MovimientoInvalido) as e:
                                print(f"Error al sacar ficha: {getattr(e, 'message', str(e))}")
                            except (FichaNoDisponible, JugadorYaGano) as e:
                                print(f"Error del jugador: {getattr(e, 'message', str(e))}")
                            except (ValueError, TypeError):
                                print("Error: Por favor ingrese números válidos.")
                            except JuegoYaTerminado as e:
                                print(f"Error: {getattr(e, 'message', str(e))}")
                                break
                        else:
                            raise OpcionInvalida("Opción inválida.")

                    except (EntradaInvalida, OpcionInvalida) as e:
                        print(getattr(e, 'message', str(e)))
                        continue
                    except (NoHayReingresoPosible, SinMovimientosDisponibles) as e:
                        print(getattr(e, 'message', str(e)))
                        break
                    except (KeyboardInterrupt, EOFError, StopIteration):
                        print("\nJuego interrumpido por el usuario.")
                        break
                    except Exception as e:
                        # Repropagar errores del dominio para que los maneje el nivel superior
                        if isinstance(e, BackgammonError):
                            raise
                        print(f"Error inesperado: {getattr(e, 'message', str(e))}")
                        continue

                # Si el juego terminó, sale del bucle
                if juego.juego_terminado():
                    break
                    
                try:
                    # Cambia el turno al siguiente jugador
                    juego.cambiar_turno()
                except (JuegoYaTerminado, TurnoIncorrecto) as e:
                    print(f"Error al cambiar turno: {getattr(e, 'message', str(e))}")
                    break
                    
            except BackgammonError as e:
                print(f"Error del juego: {getattr(e, 'message', str(e))}")
                # Pregunta si quiere continuar o salir
                respuesta = input("¿Desea continuar jugando? (s/n): ")
                if respuesta.lower() != 's':
                    break
            except (KeyboardInterrupt, EOFError, StopIteration):
                print("\nJuego interrumpido por el usuario.")
                break
            except Exception as e:
                print(f"Error inesperado en el juego: {getattr(e, 'message', str(e))}")
                respuesta = input("¿Desea continuar jugando? (s/n): ")
                if respuesta.lower() != 's':
                    break

        # Mensaje final del juego
        try:
            print("\n¡Juego terminado!")
            ganador = juego.obtener_ganador()
            if ganador:
                print(f"¡Felicidades {ganador}, has ganado!")
            else:
                print("No hay ganador.")
        except Exception as e:
            print(f"Error al finalizar el juego: {getattr(e, 'message', str(e))}")

    except Exception as e:
        print(f"Error al inicializar el juego: {getattr(e, 'message', str(e))}")
        return

if __name__ == "__main__":
    main()