from core.backgammon import Backgammon

def mostrar_tablero(tablero):
    print("\nEstado actual del tablero:")
    for i, punto in enumerate(tablero):
        print(f"{i:2}: {punto}")

def main():
    print("Bienvenido a Backgammon (CLI)\n")
    nombre1 = input("Ingrese el nombre del Jugador 1 (Blancas): ")
    nombre2 = input("Ingrese el nombre del Jugador 2 (Negras): ")

    juego = Backgammon(nombre1, "Blancas", nombre2, "Negras")

    while not juego.juego_terminado():
        jugador = juego.turno_actual
        print(f"\nTurno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
        mostrar_tablero(juego.estado_tablero())
        print(f"Fichas restantes: {jugador.mostrar_fichas_restantes()}")
        print(f"Fichas en barra: {juego.fichas_en_barra()}")

        input("Presione Enter para tirar los dados...")
        dados = juego.tirar_dados()
        print(f"Dados: {dados}")

        movimientos_realizados = 0
        dados_usados = [False] * len(dados)

        while movimientos_realizados < len(dados):
            # Si hay fichas en la barra, solo puede reingresar
            if juego.fichas_en_barra() > 0:
                print("Debe reingresar una ficha desde la barra.")
                destino = int(input("Ingrese la posición de destino para reingresar: "))
                if juego.reingresar_desde_barra(destino):
                    print("Ficha reingresada correctamente.")
                    movimientos_realizados += 1
                else:
                    print("No se pudo reingresar la ficha. Intente otra posición.")
                continue

            print("Opciones: ")
            print("1. Mover ficha")
            print("2. Sacar ficha fuera del tablero (si corresponde)")
            print("3. Pasar turno")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                origen = int(input("Origen: "))
                destino = int(input("Destino: "))
                if juego.mover(origen, destino):
                    print("Movimiento realizado.")
                    movimientos_realizados += 1
                else:
                    print("Movimiento inválido.")
            elif opcion == "2":
                origen = int(input("Origen de la ficha a sacar: "))
                if juego.sacar_ficha_fuera(origen):
                    print("Ficha sacada del tablero.")
                    movimientos_realizados += 1
                else:
                    print("No se pudo sacar la ficha. Verifique que todas estén en el home.")
            elif opcion == "3":
                print("Turno pasado.")
                break
            else:
                print("Opción inválida.")

        if juego.juego_terminado():
            break
        juego.cambiar_turno()

    print("\n¡Juego terminado!")
    ganador = juego.obtener_ganador()
    if ganador:
        print(f"¡Felicidades {ganador}, has ganado!")
    else:
        print("No hay ganador.")

if __name__ == "__main__":
    main()