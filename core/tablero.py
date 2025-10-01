#Revisar
from core.excepciones import (MovimientoInvalido, PosicionFueraDeRango, OrigenSinFicha, DestinoBloqueado, NoPuedeReingresar, NoPuedeSacarFicha)

class tablero:
    def __init__(self):
        # Inicializa el tablero con 24 posiciones vacías (listas)
        self.__tablero__ = [[] for _ in range(24)]
        # Contador de piezas comidas
        self.__piezas_comidas__ = {"Blancas": 0, "Negras": 0}
        # Fichas en la barra para cada color
        self.__barra__ = {"Blancas": 0, "Negras": 0}

    def inicializar_piezas(self):
        # Coloca las piezas en las posiciones iniciales estándar
        self.__tablero__ = [[] for _ in range(24)]
        self.__tablero__[0] = ["Blancas"] * 2
        self.__tablero__[5] = ["Negras"] * 5
        self.__tablero__[7] = ["Negras"] * 3
        self.__tablero__[11] = ["Blancas"] * 5
        self.__tablero__[12] = ["Negras"] * 5
        self.__tablero__[16] = ["Blancas"] * 3
        self.__tablero__[18] = ["Blancas"] * 5
        self.__tablero__[23] = ["Negras"] * 2
        self.__barra__ = {"Blancas": 0, "Negras": 0}
        self.__piezas_comidas__ = {"Blancas": 0, "Negras": 0}

    def mostrar_tablero(self):
        # Devuelve el estado actual del tablero
        return self.__tablero__

    def piezas_comidas(self):
        # Devuelve el diccionario de piezas comidas
        return self.__piezas_comidas__

    def sacar_pieza(self, posicion: int):
        # Saca una pieza de la posición indicada (si hay)
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        
        if self.__tablero__[posicion]:
            return self.__tablero__[posicion].pop()
        else:
            raise OrigenSinFicha(f"No hay fichas en la posición {posicion}.")

    def colocar_pieza(self, posicion: int, color: str):
        # Coloca una pieza del color dado en la posición indicada
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        
        self.__tablero__[posicion].append(color)

    def mover_pieza(self, origen: int, destino: int):
        # Mueve una pieza del origen al destino si es posible
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise PosicionFueraDeRango("Las posiciones deben estar entre 0 y 23.")
        
        if not self.__tablero__[origen]:
            raise OrigenSinFicha(f"No hay piezas para mover en la posición {origen}.")
        
        pieza = self.sacar_pieza(origen)
        
        # Verifica si el destino está bloqueado por el rival
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != pieza and
            len(self.__tablero__[destino]) > 1):
            # Devolver la pieza al origen si no se puede mover
            self.__tablero__[origen].append(pieza)
            raise DestinoBloqueado(f"La posición {destino} está bloqueada por fichas enemigas.")
        
        # Si hay una sola pieza enemiga en destino, la come
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != pieza and
            len(self.__tablero__[destino]) == 1):
            color_comido = self.__tablero__[destino].pop()
            self.__piezas_comidas__[color_comido] += 1
            self.__barra__[color_comido] += 1  # Agrega la ficha comida a la barra
        
        self.colocar_pieza(destino, pieza)

    def validar_movimiento(self, origen: int, destino: int, color: str):
        # Valida si un movimiento es posible según las reglas básicas
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise PosicionFueraDeRango("Las posiciones deben estar entre 0 y 23.")
        
        if not self.__tablero__[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen}.")
        
        if self.__tablero__[origen][-1] != color:
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
        
        # No puede mover a una posición con 2 o más piezas enemigas
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != color and
            len(self.__tablero__[destino]) > 1):
            raise DestinoBloqueado(f"La posición {destino} está bloqueada por fichas enemigas.")
        
        return True
    
    def reingresar_desde_barra(self, color: str, destino: int):
        """
        Permite colocar una ficha desde la barra en una posición de entrada válida.
        Devuelve True si pudo reingresar, False si no.
        """
        if destino < 0 or destino > 23:
            raise PosicionFueraDeRango(f"La posición {destino} está fuera del tablero (0-23).")
        
        if self.__barra__[color] <= 0:
            raise NoPuedeReingresar(f"No hay fichas de color {color} en la barra para reingresar.")
        
        # Solo puede reingresar si el destino tiene 0 o 1 ficha enemiga
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != color and
            len(self.__tablero__[destino]) > 1):
            raise DestinoBloqueado(f"No se puede reingresar en posición {destino}: está bloqueada por fichas enemigas.")
        
        # Si hay una sola ficha enemiga, la come
        if (self.__tablero__[destino] and
            self.__tablero__[destino][-1] != color and
            len(self.__tablero__[destino]) == 1):
            color_comido = self.__tablero__[destino].pop()
            self.__piezas_comidas__[color_comido] += 1
            self.__barra__[color_comido] += 1
        
        self.__tablero__[destino].append(color)
        self.__barra__[color] -= 1
        return True

    def puede_reingresar(self, color: str, dados: list):
        """
        Devuelve True si hay al menos una entrada posible desde la barra con los dados actuales.
        """
        if self.__barra__[color] == 0:
            return False
        # Determina las posiciones de entrada según el color
        posiciones = []
        if color == "Blancas":
            posiciones = [dado - 1 for dado in dados if 0 <= dado - 1 <= 23]
        else:
            posiciones = [24 - dado for dado in dados if 0 <= 24 - dado <= 23]
        for pos in posiciones:
            if (not self.__tablero__[pos] or
                self.__tablero__[pos][-1] == color or
                len(self.__tablero__[pos]) == 1):
                return True
        return False

    def todas_en_home(self, color: str):
        """
        Devuelve True si todas las fichas del color están en el home (último cuadrante).
        Para Blancas: posiciones 18-23, para Negras: posiciones 0-5.
        """
        if color == "Blancas":
            home = range(18, 24)
        else:
            home = range(0, 6)
        total = 0
        for i, punto in enumerate(self.__tablero__):
            if punto and punto[0] == color:
                if i not in home:
                    return False
                total += len([f for f in punto if f == color])
        # Además, no debe haber fichas en la barra
        return self.__barra__[color] == 0

    def sacar_ficha_fuera(self, color: str, origen: int):
        """
        Saca una ficha del tablero si está permitido (todas en home y dado lo permite).
        Devuelve True si pudo sacar, False si no.
        """
        if origen < 0 or origen > 23:
            raise PosicionFueraDeRango(f"La posición {origen} está fuera del tablero (0-23).")
        
        if not self.__tablero__[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen} para sacar.")
        
        if self.__tablero__[origen][-1] != color:
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
        
        if not self.todas_en_home(color):
            raise NoPuedeSacarFicha(f"No se puede sacar fichas: no todas las fichas de {color} están en el home.")
        
        self.__tablero__[origen].pop()
        return True

    def fichas_en_barra(self, color: str):
        """
        Devuelve la cantidad de fichas en la barra para ese color.
        """
        return self.__barra__[color]

    def mostrar_tablero_visual(self):
        """
        Devuelve una representación visual del tablero de Backgammon
        que simula el diseño clásico del juego.
        """
        # Obtener el estado actual del tablero
        tablero = self.__tablero__
        barra = self.__barra__
        
        # Crear la representación visual
        lineas = []
        
        # Línea superior con números de posiciones (12-23)
        lineas.append("┌─────────────────────────────┬───┬─────────────────────────────┬─────────────┐")
        numeros_sup = ""
        for i in range(12, 18):
            numeros_sup += f"{i:>3}"
        numeros_sup += " │BAR│ "
        for i in range(18, 24):
            numeros_sup += f"{i:>3}"
        numeros_sup += " │ HOME BLANCAS│"
        lineas.append(f"│{numeros_sup}│")
        
        # Separador
        lineas.append("├─────────────────────────────┼───┼─────────────────────────────┼─────────────┤")
        
        # Calcular fichas sacadas del tablero (para el HOME)
        fichas_blancas_iniciales = 15
        fichas_negras_iniciales = 15
        
        # Contar fichas que quedan en el tablero y en la barra
        fichas_blancas_en_juego = barra["Blancas"]
        fichas_negras_en_juego = barra["Negras"]
        
        for pos in tablero:
            fichas_blancas_en_juego += pos.count("Blancas")
            fichas_negras_en_juego += pos.count("Negras")
        
        # Fichas en HOME (sacadas del tablero)
        fichas_blancas_home = fichas_blancas_iniciales - fichas_blancas_en_juego
        fichas_negras_home = fichas_negras_iniciales - fichas_negras_en_juego
        
        # Mostrar fichas en posiciones superiores (12-23) - máximo 5 filas
        for fila in range(5):
            linea_fichas = ""
            # Posiciones 12-17
            for i in range(12, 18):
                fichas_en_pos = tablero[i]
                if len(fichas_en_pos) > fila:
                    linea_fichas += f" {fichas_en_pos[fila][0]} "
                else:
                    linea_fichas += "   "
            
            # Barra (mostrar fichas en la barra)
            barra_display = ""
            total_barra = barra["Blancas"] + barra["Negras"]
            if total_barra > fila:
                if barra["Blancas"] > fila:
                    barra_display = "B"
                elif barra["Negras"] > fila - barra["Blancas"]:
                    barra_display = "N"
                else:
                    barra_display = " "
            else:
                barra_display = " "
            linea_fichas += f" │ {barra_display} │ "
            
            # Posiciones 18-23
            for i in range(18, 24):
                fichas_en_pos = tablero[i]
                if len(fichas_en_pos) > fila:
                    linea_fichas += f" {fichas_en_pos[fila][0]} "
                else:
                    linea_fichas += "   "
            
            # HOME BLANCAS (mostrar fichas sacadas)
            home_display = ""
            if fichas_blancas_home > fila:
                home_display = f"    B:{fichas_blancas_home:2}    "
            else:
                home_display = "             "
            linea_fichas += f" │{home_display}│"
            
            lineas.append(f"│{linea_fichas}│")
        
        # Separador central
        lineas.append("├─────────────────────────────┼───┼─────────────────────────────┼─────────────┤")
        
        # Mostrar fichas en posiciones inferiores (0-11) - máximo 5 filas (invertido)
        for fila in range(4, -1, -1):
            linea_fichas = ""
            # Posiciones 11-6 (en orden inverso)
            for i in range(11, 5, -1):
                fichas_en_pos = tablero[i]
                if len(fichas_en_pos) > fila:
                    linea_fichas += f" {fichas_en_pos[fila][0]} "
                else:
                    linea_fichas += "   "
            
            # Barra (repetir la lógica)
            barra_display = ""
            total_barra = barra["Blancas"] + barra["Negras"]
            if total_barra > (4-fila):
                if barra["Blancas"] > (4-fila):
                    barra_display = "B"
                elif barra["Negras"] > (4-fila) - barra["Blancas"]:
                    barra_display = "N"
                else:
                    barra_display = " "
            else:
                barra_display = " "
            linea_fichas += f" │ {barra_display} │ "
            
            # Posiciones 5-0 (en orden inverso)
            for i in range(5, -1, -1):
                fichas_en_pos = tablero[i]
                if len(fichas_en_pos) > fila:
                    linea_fichas += f" {fichas_en_pos[fila][0]} "
                else:
                    linea_fichas += "   "
            
            # HOME NEGRAS (mostrar fichas sacadas)
            home_display = ""
            if fichas_negras_home > (4-fila):
                home_display = f"    N:{fichas_negras_home:2}    "
            else:
                home_display = "             "
            linea_fichas += f" │{home_display}│"
            
            lineas.append(f"│{linea_fichas}│")
        
        # Separador
        lineas.append("├─────────────────────────────┼───┼─────────────────────────────┼─────────────┤")
        
        # Línea inferior con números de posiciones (0-11)
        numeros_inf = ""
        for i in range(11, 5, -1):
            numeros_inf += f"{i:>3}"
        numeros_inf += " │   │ "
        for i in range(5, -1, -1):
            numeros_inf += f"{i:>3}"
        numeros_inf += " │ HOME NEGRAS │"
        lineas.append(f"│{numeros_inf}│")
        
        # Línea final
        lineas.append("└─────────────────────────────┴───┴─────────────────────────────┴─────────────┘")
        
        # Información adicional
        lineas.append(f"\nFichas en barra - Blancas: {barra['Blancas']}, Negras: {barra['Negras']}")
        lineas.append(f"Fichas comidas - Blancas: {self.__piezas_comidas__['Blancas']}, Negras: {self.__piezas_comidas__['Negras']}")
        lineas.append(f"Puntos ganados - Blancas: {fichas_blancas_home}, Negras: {fichas_negras_home}")
        
        return "\n".join(lineas)