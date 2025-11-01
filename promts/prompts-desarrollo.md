## Registro de Prompts de IA — Desarrollo

Este documento registra los prompts de desarrollo utilizados para implementar o refactorizar funcionalidad del proyecto. Por cada entrada se indica: modelo/herramienta, instrucciones del sistema (si hubo), prompt exacto (o equivalente), respuesta de la IA (resumen), uso (tal cual/modificado/descartado) y archivos referenciados.

Referencias de estilo basadas únicamente en materiales compartidos por el usuario (enlaces a chats). Nota: el contenido completo de los chats no fue accesible sin autenticación y se usó solo como guía de formato.

---

## PD-01 – Normalización e integración de la UI Pygame (`GameUI`)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Arreglar `pygame_ui/game_ui.py` con indentación consistente (espacios), eliminar bloques duplicados, definir la clase `GameUI` completamente y añadir `run()` para que `main_pygame.py` pueda ejecutar el bucle principal.
- Prompt (resumen):
	“Repara `pygame_ui/game_ui.py`: unifica espacios, elimina código mal duplicado, asegura que exista `GameUI.run()` y que el `__main__` esté correcto. Compila y corrige cualquier error de indentación o bloques ‘inconsistentes’.”
- Instrucciones del sistema: Mantener cambios mínimos, no romper APIs; validar compilación y lint.
- Respuesta/Resultado: Se reescribió el archivo con indentación uniforme, se definió `run()` y se limpió el bloque `main`. Se corrigió `main_pygame.py` para el llamado `ui.run()`.
- Uso: Aplicado con modificaciones menores.
- Archivos finales referenciados:
	- `pygame_ui/game_ui.py`
	- `pygame_ui/main_pygame.py`

---

## PD-02 – Pasar turno automático cuando no hay reingreso desde barra

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Implementar la regla: si el jugador tiene fichas en barra y los dados no permiten reingresar (puntos bloqueados), pierde el turno automáticamente.
- Prompt (resumen):
	“En `GameUI`, cuando se tiran dados, si el jugador tiene fichas en la barra y no existen destinos válidos de reingreso, pasar turno automáticamente, limpiar estado de dados/selección y actualizar mensaje.”
- Instrucciones del sistema: Mantener la lógica en UI (no romper `core/`), actualizar mensajes y recalcular selección de barra en el nuevo turno.
- Respuesta/Resultado: Se extendió `handle_space()` para detectar la ausencia de movimientos (con barra o en general) y llamar a `cambiar_turno()` con limpieza de estado.
- Uso: Aplicado.
- Archivos finales referenciados:
	- `pygame_ui/game_ui.py`

---

## PD-03 – Correcciones menores en núcleo para estabilidad/lint

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Resolver pequeños defectos de indentación/retornos y warnings de estilo en núcleo.
- Prompt (resumen):
	“Corregí indentaciones y returns dedentados en `core/backgammon.py`; arreglá `__str__` en `core/jugador.py`; normalizá `reiniciar_turno` y naming en `core/dice.py` con pragmas locales.”
- Instrucciones del sistema: Cambios mínimos, sin alterar API pública.
- Respuesta/Resultado: Ajustes pequeños que eliminaron errores de compilación y mejoraron Pylint.
- Uso: Aplicado con modificaciones menores.
- Archivos finales referenciados:
	- `core/backgammon.py`
	- `core/jugador.py`
	- `core/dice.py`

---

## PD-04 – Limpieza de UI Pygame auxiliar

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Normalizar indentación y estilo en UI auxiliar: `events_handler.py`, `dice_renderer.py`, `main_pygame.py`, `board_view.py` (cuando correspondió).
- Prompt (resumen):
	“Normalizá indentación a 4 espacios, elimina restos/artefactos y asegura que los módulos de pygame compilen. Si hace falta, usa pragmas pylint locales no intrusivos.”
- Instrucciones del sistema: Mantener comportamiento; validar con `python -m py_compile` tareas.
- Respuesta/Resultado: Todos los módulos de UI compilan; Pylint del paquete UI ≥ 8.75.
- Uso: Aplicado.
- Archivos finales referenciados:
	- `pygame_ui/events_handler.py`
	- `pygame_ui/dice_renderer.py`
	- `pygame_ui/main_pygame.py`
	- `pygame_ui/board_view.py`

---

## PD-05 – Mejora de calidad: Lint y mensajes de estado

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Incrementar legibilidad y mensajes de estado en la UI (instrucciones en barra inferior; feedback al pasar turno automático).
- Prompt (resumen):
	“Ajustá los mensajes de `GameUI` para que informen al usuario: cuándo tirar dados, cómo seleccionar/mover y cuándo se pasa turno por no haber movimientos.”
- Instrucciones del sistema: Mensajes en español, consistentes con reglas del juego.
- Respuesta/Resultado: Mensajes actualizados en `handle_space` y post-movimiento; se añadió inicialización segura de `_overlay_buttons`.
- Uso: Aplicado.
- Archivos finales referenciados:
	- `pygame_ui/game_ui.py`

---

## PD-06 – Integración con cobertura y CI (resumen)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Objetivo: Asegurar cobertura > 92% en núcleo, mantener CI con Pylint y reportes de cobertura.
- Prompt (resumen):
	“Elevar cobertura con tests dirigidos; configurar CI para ejecutar tests/coverage y pylint; subir reportes como artefactos.”
- Instrucciones del sistema: Cambios mínimos, mantener `.coveragerc` para excluir UI y CLI si corresponde.
- Respuesta/Resultado: Cobertura central ~96%; Pylint global ~9.3; CI preparado para incluir UI en lint.
- Uso: Aplicado con modificaciones menores.
- Archivos finales referenciados:
	- `test/` (suite existente)
	- `.coveragerc`
	- `README.md` (instrucciones)
	- `.github/workflows/ci.yml`

---

### Referencias externas
- Chats IA compartidos por el usuario:
  - ChatGPT: https://chatgpt.com/share/69068e1d-ac4c-8011-838a-98ae9bfed681
  - Gemini: https://gemini.google.com/share/40163a1c1595, https://gemini.google.com/share/b66d3ec7f154
  Nota: Los contenidos completos no son accesibles sin autenticación; se usaron como guía de formato y alcance.
