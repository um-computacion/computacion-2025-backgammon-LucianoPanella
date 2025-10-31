from core.backgammon import Backgammon
from core.constants import BLANCAS, NEGRAS, BOARD_POINTS
from core.excepciones import (
    BackgammonError, MovimientoInvalido, PosicionFueraDeRango, 
    OrigenSinFicha, DestinoBloqueado, NoPuedeReingresar, 
    NoPuedeSacarFicha, FichaNoDisponible, JugadorYaGano,
    DadosNoTirados, DadoNoDisponible, TurnoIncorrecto, 
    JuegoYaTerminado
)

def mostrar_tablero(juego):
    # Muestra el estado actual del tablero en formato visual de Backgammon
    print(juego.estado_tablero_visual())

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

                # Mientras queden dados por usar, el jugador puede hacer movimientos
                while dados_disponibles:
                    try:
                        mostrar_tablero(juego)  # CAMBIO: pasamos el objeto juego completo
                        print(f"\nTurno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
                        print(f"Dados restantes: {dados_disponibles}")
                        print("Opciones: ")
                        print("1. Mover ficha")
                        print("2. Sacar ficha fuera del tablero (si corresponde)")
                        print("3. Pasar turno")

                        # Si hay fichas en la barra, solo puede reingresar
                        if juego.fichas_en_barra() > 0:
                            try:
                                print("Debe reingresar una ficha desde la barra.")
                                while True:
                                    try:
                                        destino = int(input("Ingrese la posición de destino para reingresar: "))
                                        if 0 <= destino < BOARD_POINTS:
                                            break
                                        print(f"La posición debe estar entre 0 y {BOARD_POINTS-1}.")
                                    except (ValueError, TypeError):
                                        print("Error: Por favor ingrese un número válido.")
                                # Elige qué dado usar para reingresar
                                print(f"Dados disponibles para reingresar: {dados_disponibles}")
                                while True:
                                    try:
                                        dado_usado = int(input("¿Qué dado desea usar para reingresar? "))
                                        break
                                    except (ValueError, TypeError):
                                        print("Error: Por favor ingrese un número válido.")
                                
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

                        try:
                            opcion = input("Seleccione una opción: ")

                            if opcion == "1":
                                # Mover ficha usando un dado específico
                                try:
                                    while True:
                                        try:
                                            origen = int(input("Origen: "))
                                            if 0 <= origen < BOARD_POINTS:
                                                break
                                            print(f"El origen debe estar entre 0 y {BOARD_POINTS-1}.")
                                        except (ValueError, TypeError):
                                            print("Error: Por favor ingrese un número válido.")
                                    print(f"Dados disponibles para mover: {dados_disponibles}")
                                    while True:
                                        try:
                                            dado_usado = int(input("¿Qué dado desea usar para mover? "))
                                            break
                                        except (ValueError, TypeError):
                                            print("Error: Por favor ingrese un número válido.")
                                    
                                    if dado_usado in dados_disponibles:
                                        color = jugador.obtener_color()
                                        # Calcula el destino según el color del jugador
                                        if color == BLANCAS:
                                            destino = origen + dado_usado
                                        else:
                                            destino = origen - dado_usado
                                        # Verifica si el movimiento es válido y lo realiza
                                        if 0 <= destino < BOARD_POINTS and juego.mover(origen, destino):
                                            print(f"Movimiento realizado de {origen} a {destino} usando dado {dado_usado}.")
                                            dados_disponibles.remove(dado_usado)
                                        else:
                                            print("Movimiento inválido.")
                                        mostrar_tablero(juego)  # CAMBIO: pasamos el objeto juego completo
                                    else:
                                        print("Dado no válido.")
                                        
                                except (MovimientoInvalido, PosicionFueraDeRango, OrigenSinFicha, DestinoBloqueado) as e:
                                    print(f"Error en el movimiento: {getattr(e, 'message', str(e))}")
                                except (ValueError, TypeError):
                                    print("Error: Por favor ingrese números válidos.")
                                except JuegoYaTerminado as e:
                                    print(f"Error: {getattr(e, 'message', str(e))}")
                                    break

                            elif opcion == "2":
                                # Sacar ficha fuera del tablero usando un dado específico
                                try:
                                    while True:
                                        try:
                                            origen = int(input("Origen de la ficha a sacar: "))
                                            if 0 <= origen < BOARD_POINTS:
                                                break
                                            print(f"El origen debe estar entre 0 y {BOARD_POINTS-1}.")
                                        except (ValueError, TypeError):
                                            print("Error: Por favor ingrese un número válido.")
                                    print(f"Dados disponibles para sacar ficha: {dados_disponibles}")
                                    while True:
                                        try:
                                            dado_usado = int(input("¿Qué dado desea usar para sacar ficha? "))
                                            break
                                        except (ValueError, TypeError):
                                            print("Error: Por favor ingrese un número válido.")
                                    
                                    if dado_usado in dados_disponibles:
                                        if juego.sacar_ficha_fuera(origen):
                                            print("Ficha sacada del tablero.")
                                            dados_disponibles.remove(dado_usado)
                                        else:
                                            print("No se pudo sacar la ficha. Verifique que todas estén en el home.")
                                        mostrar_tablero(juego)  # CAMBIO: pasamos el objeto juego completo
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

                            elif opcion == "3":
                                # El jugador decide pasar el turno
                                print("Turno pasado.")
                                break
                            else:
                                print("Opción inválida.")
                                
                        except KeyboardInterrupt:
                            print("\nJuego interrumpido por el usuario.")
                            return
                        except Exception as e:
                            print(f"Error inesperado: {getattr(e, 'message', str(e))}")
                            
                    except BackgammonError as e:
                        print(f"Error del juego: {getattr(e, 'message', str(e))}")
                    except Exception as e:
                        print(f"Error inesperado en el turno: {getattr(e, 'message', str(e))}")

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
            except KeyboardInterrupt:
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