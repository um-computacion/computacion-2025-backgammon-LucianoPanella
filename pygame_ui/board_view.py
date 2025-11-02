#FINALIZADO#
import pygame
from core.constants import INITIAL_CHECKERS
from pygame_ui.dice_renderer import DiceRenderer
from pygame_ui.constants import (
    UI_MARGIN, UI_MESSAGE_BAR_HEIGHT, UI_BOTTOM_LABELS_BAND, UI_TOP_LABELS_BAND,
    UI_OFF_TRAY_WIDTH, UI_MAX_VISIBLE_STACK, UI_STACK_SPACING_FACTOR,
    COLOR_BOARD_BG, COLOR_TRIANGLE_LIGHT, COLOR_TRIANGLE_DARK,
    COLOR_BLACK, COLOR_WHITE, COLOR_GRAY, COLOR_BAR_BG, COLOR_TRAY_BG,
    COLOR_MSG_BAR_BG, COLOR_TURN_INDICATOR, COLOR_HL_DEST, COLOR_HL_SEL, COLOR_HL_SEL_BORDER,
)


class BoardView:
    """Render del tablero, fichas, bandeja de borne-off, barra central y HUD de mensajes.

    No modifica lógica de juego; sólo dibuja en pantalla usando un objeto `game`
    compatible con core.Backgammon (estado_tablero, fichas_en_barra, jugadores).
    """

    def __init__(self, width=900, height=600):
        self.width = width
        self.height = height

        # Geometría general
        self.margin = UI_MARGIN
        self.message_bar_height = UI_MESSAGE_BAR_HEIGHT
        self.bottom_labels_band = UI_BOTTOM_LABELS_BAND
        self.top_labels_band = UI_TOP_LABELS_BAND  # banda superior reservada para números
        self.off_tray_width = UI_OFF_TRAY_WIDTH
        # La barra central tendrá el mismo ancho que la bandeja derecha
        self.center_bar_width = self.off_tray_width

        # Tamaño de triángulos dejando espacio para bandeja y barra central
        self.triangle_width = (
            self.width - 2 * self.margin - self.off_tray_width - self.center_bar_width
        ) / 12
        self.triangle_height = (
            self.height
            - (
                self.message_bar_height
                + self.bottom_labels_band
                + self.top_labels_band
                + self.margin
            )
        ) / 2

        # Tipografías
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 18)
        self.message_font = pygame.font.SysFont("arial", 22, bold=True)
        # Renderizador de dados externo
        self._dice_renderer = DiceRenderer()

    # --- utilidades de geometría ---
    def _col_x(self, col: int) -> float:
        """X inicial de la columna 0..11 considerando la barra central."""
        base = self.margin + col * self.triangle_width
        if col >= 6:
            base += self.center_bar_width
        return base

    def _col_center(self, col: int) -> float:
        return self._col_x(col) + self.triangle_width / 2

    # ------------------------------------------------------------------
    def draw_board(self, screen):
        """Dibuja el fondo, triángulos, barra central, bandeja y numeración."""
        screen.fill(COLOR_BOARD_BG)

        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
        tablero_height = tablero_bottom - tablero_top

        # Triángulos superiores (debajo de la banda de números)
        top_y = tablero_top + self.top_labels_band
        for i in range(12):
            color = COLOR_TRIANGLE_DARK if i % 2 == 0 else COLOR_TRIANGLE_LIGHT
            x = self._col_x(i)
            pts = [
                (x, top_y),
                (x + self.triangle_width, top_y),
                (x + self.triangle_width / 2, top_y + self.triangle_height),
            ]
            pygame.draw.polygon(screen, color, pts)

        # Triángulos inferiores
        for i in range(12):
            color = COLOR_TRIANGLE_LIGHT if i % 2 == 0 else COLOR_TRIANGLE_DARK
            x = self._col_x(i)
            base_y = tablero_bottom
            pts = [
                (x, base_y),
                (x + self.triangle_width, base_y),
                (x + self.triangle_width / 2, base_y - self.triangle_height),
            ]
            pygame.draw.polygon(screen, color, pts)

        # Barra central (bar)
        bar_left = self.margin + 6 * self.triangle_width
        pygame.draw.rect(
            screen,
            COLOR_BAR_BG,
            pygame.Rect(bar_left, tablero_top, self.center_bar_width, tablero_height),
            border_radius=2,
        )

        # Bandeja de borne-off a la derecha
        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        tray_rect = pygame.Rect(tray_left, tablero_top, self.off_tray_width, tablero_height)
        pygame.draw.rect(screen, COLOR_TRAY_BG, tray_rect)
        pygame.draw.rect(screen, COLOR_BLACK, tray_rect, 2)

        # Números superiores (1..12 de derecha a izquierda)
        for i in range(12):
            num = self.font.render(str(12 - i), True, COLOR_BLACK)
            screen.blit(num, (self._col_x(i) + 10, tablero_top + 5))

        # Números inferiores (13..24 de izquierda a derecha)
        bottom_num_y = self.height - self.message_bar_height - self.bottom_labels_band + 18
        for i in range(12):
            num = self.font.render(str(13 + i), True, COLOR_BLACK)
            screen.blit(num, (self._col_x(i) + 10, bottom_num_y))

    # ------------------------------------------------------------------
    def draw_checkers(self, screen, game):
        """Dibuja las fichas en puntos, barra central y bandeja de borne-off.

        game: instancia de core.Backgammon
        """
        # Estado del tablero
        if hasattr(game, "estado_tablero"):
            board = game.estado_tablero()
        elif hasattr(game, "tablero") and hasattr(game.tablero, "mostrar_tablero"):
            board = game.tablero.mostrar_tablero()
        else:
            board = [[] for _ in range(24)]

        # Puntos 0-11 abajo, 12-23 arriba
        radius = int(min(self.triangle_width * 0.33, (self.off_tray_width * 0.45)))
        max_visible = UI_MAX_VISIBLE_STACK

        for i, fichas in enumerate(board):
            count = len(fichas)
            if count == 0:
                continue

            # En nuestro core, fichas son 'Blancas' o 'Negras'
            color = COLOR_WHITE if fichas[0] == "Blancas" else COLOR_BLACK

            # Coordenadas base para apilar
            if i < 12:  # parte inferior
                col = 11 - i
                x = self._col_center(col)
                y_base = self.height - self.message_bar_height - self.bottom_labels_band - 10
                dy = -radius * UI_STACK_SPACING_FACTOR
            else:  # parte superior
                col = i - 12
                x = self._col_center(col)
                y_base = self.margin + self.top_labels_band + radius * 1.1
                dy = radius * UI_STACK_SPACING_FACTOR

            visibles = min(count, max_visible)
            for j in range(visibles):
                y = y_base + j * dy
                pygame.draw.circle(screen, color, (int(x), int(y)), int(radius))
                pygame.draw.circle(screen, COLOR_GRAY, (int(x), int(y)), int(radius), 2)

            # Si hay más fichas, mostrar número en la última visible
            if count > max_visible:
                y = y_base + (max_visible - 1) * dy
                text_color = COLOR_BLACK if color == COLOR_WHITE else COLOR_WHITE
                label = self.font.render(str(count), True, text_color)
                rect = label.get_rect(center=(x, y))
                screen.blit(label, rect)

        # --- Barra central ---
        try:
            blancas_en_barra = game.fichas_en_barra("Blancas")
            negras_en_barra = game.fichas_en_barra("Negras")
        except Exception:
            blancas_en_barra = 0
            negras_en_barra = 0

        bar_left = self.margin + 6 * self.triangle_width
        cx = bar_left + self.center_bar_width / 2

        # Top (blancas) hacia abajo
        y_top_base = self.margin + self.top_labels_band + radius * 1.1
        for j in range(min(max_visible, blancas_en_barra)):
            y = y_top_base + j * (radius * UI_STACK_SPACING_FACTOR)
            pygame.draw.circle(screen, COLOR_WHITE, (int(cx), int(y)), radius)
            pygame.draw.circle(screen, COLOR_GRAY, (int(cx), int(y)), radius, 2)
        if blancas_en_barra > max_visible:
            y = y_top_base + (max_visible - 1) * (radius * UI_STACK_SPACING_FACTOR)
            label = self.font.render(str(blancas_en_barra), True, COLOR_BLACK)
            rect = label.get_rect(center=(cx, y))
            screen.blit(label, rect)

        # Bottom (negras) hacia arriba
        y_bottom_base = self.height - self.message_bar_height - self.bottom_labels_band - 10
        for j in range(min(max_visible, negras_en_barra)):
            y = y_bottom_base - j * (radius * UI_STACK_SPACING_FACTOR)
            pygame.draw.circle(screen, COLOR_BLACK, (int(cx), int(y)), radius)
            pygame.draw.circle(screen, COLOR_GRAY, (int(cx), int(y)), radius, 2)
        if negras_en_barra > max_visible:
            y = y_bottom_base - (max_visible - 1) * (radius * UI_STACK_SPACING_FACTOR)
            label = self.font.render(str(negras_en_barra), True, COLOR_WHITE)
            rect = label.get_rect(center=(cx, y))
            screen.blit(label, rect)

        # --- Bandeja de borne-off derecha ---
        try:
            j1 = getattr(game, "jugador1", None)
            j2 = getattr(game, "jugador2", None)
            fuera_blancas = 0
            fuera_negras = 0
            for j in (j1, j2):
                if j is None:
                    continue
                restantes = j.mostrar_fichas_restantes()
                fuera = max(0, INITIAL_CHECKERS - int(restantes))
                color_j = j.obtener_color()
                if color_j == "Blancas":
                    fuera_blancas = fuera
                elif color_j == "Negras":
                    fuera_negras = fuera
        except Exception:
            fuera_blancas = 0
            fuera_negras = 0

        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        tray_center_x = tray_left + self.off_tray_width / 2

        # Negras arriba (hacia abajo)
        y_base_top = self.margin + radius * 1.1
        for j in range(min(max_visible, fuera_negras)):
            y = y_base_top + j * (radius * UI_STACK_SPACING_FACTOR)
            pygame.draw.circle(screen, COLOR_BLACK, (int(tray_center_x), int(y)), radius)
            pygame.draw.circle(screen, COLOR_GRAY, (int(tray_center_x), int(y)), radius, 2)
        if fuera_negras > max_visible:
            y = y_base_top + (max_visible - 1) * (radius * UI_STACK_SPACING_FACTOR)
            label = self.font.render(str(fuera_negras), True, COLOR_WHITE)
            rect = label.get_rect(center=(tray_center_x, y))
            screen.blit(label, rect)

        # Blancas abajo (hacia arriba)
        y_base_bottom = self.height - self.message_bar_height - self.bottom_labels_band - 10
        for j in range(min(max_visible, fuera_blancas)):
            y = y_base_bottom - j * (radius * UI_STACK_SPACING_FACTOR)
            pygame.draw.circle(screen, COLOR_WHITE, (int(tray_center_x), int(y)), radius)
            pygame.draw.circle(screen, COLOR_GRAY, (int(tray_center_x), int(y)), radius, 2)
        if fuera_blancas > max_visible:
            y = y_base_bottom - (max_visible - 1) * (radius * UI_STACK_SPACING_FACTOR)
            label = self.font.render(str(fuera_blancas), True, COLOR_BLACK)
            rect = label.get_rect(center=(tray_center_x, y))
            screen.blit(label, rect)

    # ------------------------------------------------------------------
    def draw_message_bar(self, screen, message):
        """Dibuja la barra de mensajes inferior."""
        bar_rect = pygame.Rect(
            0, self.height - self.message_bar_height, self.width, self.message_bar_height
        )
        pygame.draw.rect(screen, COLOR_MSG_BAR_BG, bar_rect)
        pygame.draw.line(
            screen,
            COLOR_BLACK,
            (0, self.height - self.message_bar_height),
            (self.width, self.height - self.message_bar_height),
            2,
        )
        text = self.message_font.render(message, True, COLOR_BLACK)
        rect = text.get_rect(
            center=(self.width // 2, self.height - self.message_bar_height // 2)
        )
        screen.blit(text, rect)

    # ------------------------------------------------------------------
    def get_point_from_mouse(self, pos):
        """Traduce un clic en coordenadas a índice de punto (0–23), 'barra' u 'off'."""
        x, y = pos
        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band

        if y < tablero_top or y > tablero_bottom:
            return None

        # Barra central
        bar_left = self.margin + 6 * self.triangle_width
        bar_right = bar_left + self.center_bar_width
        if bar_left <= x <= bar_right:
            return 'barra'

        # Bandeja borne-off
        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        if x >= tray_left:
            return 'off'

        # zona superior/inferior con tolerancia
        overflow = int(min(self.triangle_height * 0.2, 24))
        top_limit = tablero_top + self.top_labels_band + self.triangle_height + overflow
        bottom_limit = tablero_bottom - self.triangle_height - overflow
        if y < top_limit:
            row = "top"
        elif y > bottom_limit:
            row = "bottom"
        else:
            return None

        # Calcular columna (0..11) con gap de barra central
        if x < bar_left:
            col = int((x - self.margin) / self.triangle_width)
        elif x > bar_right:
            col = int((x - (self.margin + self.center_bar_width)) / self.triangle_width)
        else:
            return 'barra'

        if col < 0 or col > 11:
            return None

        if row == "top":
            return 12 + col
        else:
            return 11 - col

    # ------------------------------------------------------------------
    def draw_dados(self, screen, valores):
        """Delegado al DiceRenderer para dibujar dados en la barra central."""
        self._dice_renderer.draw_on_bar(self, screen, valores)

    # ------------------------------------------------------------------
    def draw_names(self, screen, nombre_blancas: str, nombre_negras: str, active_color: str | None = None):
        """Nombres de jugadores en la banda superior (fuera del tablero) con indicador de turno."""
        top_y = 8
        left_pos = (self.margin, top_y)
        right_text = None

        if nombre_negras:
            txt_neg = self.message_font.render(f"Negras: {nombre_negras}", True, COLOR_BLACK)
            screen.blit(txt_neg, left_pos)
            # Indicador de turno para Negras
            if active_color == 'Negras':
                cx = left_pos[0] - 14
                cy = left_pos[1] + txt_neg.get_height() // 2
                pygame.draw.circle(screen, COLOR_TURN_INDICATOR, (cx, cy), 6)

        if nombre_blancas:
            txt_bla = self.message_font.render(f"Blancas: {nombre_blancas}", True, COLOR_BLACK)
            x = self.width - self.margin - txt_bla.get_width()
            screen.blit(txt_bla, (x, top_y))
            # Indicador de turno para Blancas
            if active_color == 'Blancas':
                cx = x + txt_bla.get_width() + 14
                cy = top_y + txt_bla.get_height() // 2
                pygame.draw.circle(screen, COLOR_TURN_INDICATOR, (cx, cy), 6)

    # ------------------------------------------------------------------
    def draw_highlights(self, screen, puntos, seleccionado=None):
        """Resalta destinos posibles y el origen seleccionado.

        - puntos: iterable con índices 0..23 y/o 'off'/'barra'.
        - seleccionado: None o índice 0..23 o 'barra'.
        """
        if not puntos and seleccionado is None:
            return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Resaltar destinos
        for p in (puntos or []):
            if p == 'off':
                # Bandeja derecha
                tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
                tablero_top = self.margin
                tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
                h = tablero_bottom - tablero_top
                rect = pygame.Rect(tray_left, tablero_top, self.off_tray_width, h)
                s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                s.fill(COLOR_HL_DEST)
                overlay.blit(s, rect.topleft)
                continue
            if p == 'barra':
                bar_left = self.margin + 6 * self.triangle_width
                tablero_top = self.margin
                tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
                h = tablero_bottom - tablero_top
                rect = pygame.Rect(bar_left, tablero_top, self.center_bar_width, h)
                s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                s.fill(COLOR_HL_DEST)
                overlay.blit(s, rect.topleft)
                continue

            # Punto 0..23: dibujar un rectángulo translúcido que llegue hasta la mitad del tablero
            if isinstance(p, int) and 0 <= p <= 23:
                if p < 12:
                    col = 11 - p
                    x = self._col_x(col)
                    w = self.triangle_width
                    base_y = self.height - self.message_bar_height - self.bottom_labels_band
                    h = self.triangle_height  # desde base hasta mitad de tablero
                    rect = pygame.Rect(int(x), int(base_y - h), int(w), int(h))
                else:
                    col = p - 12
                    x = self._col_x(col)
                    w = self.triangle_width
                    top_y = self.margin + self.top_labels_band
                    h = self.triangle_height  # desde arriba hasta mitad de tablero
                    rect = pygame.Rect(int(x), int(top_y), int(w), int(h))
                s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                s.fill(COLOR_HL_DEST)
                overlay.blit(s, rect.topleft)

        # Resaltar origen seleccionado
        if seleccionado is not None:
            if seleccionado == 'barra':
                bar_left = self.margin + 6 * self.triangle_width
                tablero_top = self.margin
                tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
                h = tablero_bottom - tablero_top
                rect = pygame.Rect(bar_left, tablero_top, self.center_bar_width, h)
                pygame.draw.rect(overlay, COLOR_HL_SEL_BORDER, rect, 6)
            elif isinstance(seleccionado, int) and 0 <= seleccionado <= 23:
                # Resaltar con un marco rectangular más notorio en la base del triángulo
                if seleccionado < 12:
                    col = 11 - seleccionado
                    x = self._col_x(col)
                    w = self.triangle_width
                    base_y = self.height - self.message_bar_height - self.bottom_labels_band
                    h = max(18, self.triangle_height * 0.35)
                    rect = pygame.Rect(int(x), int(base_y - h), int(w), int(h))
                else:
                    col = seleccionado - 12
                    x = self._col_x(col)
                    w = self.triangle_width
                    top_y = self.margin + self.top_labels_band
                    h = max(18, self.triangle_height * 0.35)
                    rect = pygame.Rect(int(x), int(top_y), int(w), int(h))
                pygame.draw.rect(overlay, COLOR_HL_SEL, rect, 5)

        screen.blit(overlay, (0, 0))
