# Automated Reports
## Coverage Report
text
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
core/__init__.py          0      0   100%
core/backgammon.py       85      0   100%
core/constants.py         7      0   100%
core/dice.py             31      0   100%
core/excepciones.py      21      0   100%
core/jugador.py          25      1    96%   38
core/tablero.py         198     13    93%   57, 63, 73, 81, 153-155, 165, 171, 187, 280, 326, 342
---------------------------------------------------
TOTAL                   367     14    96%


## Pylint Report
text
************* Module core.tablero
core/tablero.py:61:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:79:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:111:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:127:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:133:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:343:0: C0303: Trailing whitespace (trailing-whitespace)
core/tablero.py:368:0: C0301: Line too long (133/120) (line-too-long)
core/tablero.py:371:0: C0304: Final newline missing (missing-final-newline)
core/tablero.py:64:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/tablero.py:224:8: W0621: Redefining name 'tablero' from outer scope (line 19) (redefined-outer-name)
core/tablero.py:234:12: R1713: Consider using str.join(sequence) for concatenating strings from an iterable (consider-using-join)
core/tablero.py:356:12: R1713: Consider using str.join(sequence) for concatenating strings from an iterable (consider-using-join)
************* Module core.jugador
core/jugador.py:9:92: C0303: Trailing whitespace (trailing-whitespace)
core/jugador.py:30:0: C0303: Trailing whitespace (trailing-whitespace)
core/jugador.py:34:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module core.excepciones
core/excepciones.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:23:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:27:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:31:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:35:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:39:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:45:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:49:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:55:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:65:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:69:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:75:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:79:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:83:0: C0303: Trailing whitespace (trailing-whitespace)
core/excepciones.py:87:0: C0303: Trailing whitespace (trailing-whitespace)
************* Module core.dice
core/dice.py:33:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module core.backgammon
core/backgammon.py:47:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:57:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:89:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:130:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:188:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:196:0: C0304: Final newline missing (missing-final-newline)
core/backgammon.py:158:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/backgammon.py:176:29: W0621: Redefining name 'jugador' from outer scope (line 6) (redefined-outer-name)
************* Module cli.cli
cli/cli.py:5:62: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:6:56: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:8:54: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:45:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:73:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:97:0: C0301: Line too long (131/120) (line-too-long)
cli/cli.py:139:0: C0301: Line too long (132/120) (line-too-long)
cli/cli.py:156:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
cli/cli.py:157:0: C0301: Line too long (129/120) (line-too-long)
cli/cli.py:193:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
cli/cli.py:194:0: C0301: Line too long (129/120) (line-too-long)
cli/cli.py:245:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:252:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:284:0: C0304: Final newline missing (missing-final-newline)
cli/cli.py:35:27: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:279:11: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:262:19: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:235:27: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:46:4: R1702: Too many nested blocks (10/5) (too-many-nested-blocks)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:159:36: W0707: Consider explicitly re-raising using 'except (ValueError, TypeError) as exc' and 'raise EntradaInvalida('Origen inválido: debe ser un número.') from exc' (raise-missing-from)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:165:36: W0707: Consider explicitly re-raising using 'except (ValueError, TypeError) as exc' and 'raise EntradaInvalida('Dado inválido: debe ser un número.') from exc' (raise-missing-from)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:196:36: W0707: Consider explicitly re-raising using 'except (ValueError, TypeError) as exc' and 'raise EntradaInvalida('Origen inválido: debe ser un número.') from exc' (raise-missing-from)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:202:36: W0707: Consider explicitly re-raising using 'except (ValueError, TypeError) as exc' and 'raise EntradaInvalida('Dado inválido: debe ser un número.') from exc' (raise-missing-from)
cli/cli.py:46:4: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
cli/cli.py:276:15: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:43:0: R1711: Useless return at end of function or method (useless-return)
cli/cli.py:4:0: W0611: Unused DadoNoDisponible imported from core.excepciones (unused-import)
cli/cli.py:4:0: W0611: Unused DebeReingresarPrimero imported from core.excepciones (unused-import)
************* Module pygame_ui.game_ui
pygame_ui/game_ui.py:96:2: W0612: Unused variable 'board' (unused-variable)
pygame_ui/game_ui.py:419:19: C0209: Formatting a regular string which could be an f-string (consider-using-f-string)
pygame_ui/game_ui.py:468:29: E1136: Value 'btns' is unsubscriptable (unsubscriptable-object)
pygame_ui/game_ui.py:470:28: E1136: Value 'btns' is unsubscriptable (unsubscriptable-object)
************* Module pygame_ui.constants
pygame_ui/constants.py:52:0: C0305: Trailing newlines (trailing-newlines)
************* Module pygame_ui.board_view
pygame_ui/board_view.py:181:15: W0718: Catching too general exception Exception (broad-exception-caught)
pygame_ui/board_view.py:228:15: W0718: Catching too general exception Exception (broad-exception-caught)
pygame_ui/board_view.py:322:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
pygame_ui/board_view.py:280:4: R0911: Too many return statements (8/6) (too-many-return-statements)
pygame_ui/board_view.py:337:8: W0612: Unused variable 'right_text' (unused-variable)
************* Module pygame_ui.main_pygame
pygame_ui/main_pygame.py:181:0: C0305: Trailing newlines (trailing-newlines)
pygame_ui/main_pygame.py:48:12: R1720: Unnecessary "elif" after "raise", remove the leading "el" from "elif" (no-else-raise)
pygame_ui/main_pygame.py:46:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main_pygame.py:14:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)


