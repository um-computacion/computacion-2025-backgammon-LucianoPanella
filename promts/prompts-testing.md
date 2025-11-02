## Registro de Prompts de IA — Testing

Este documento registra los prompts relacionados a pruebas y cobertura. Para cada ítem: modelo/herramienta, instrucciones del sistema, prompt exacto (o citado), resultado/uso y archivos involucrados.

Referencias de formato: enlaces a chats externos compartidos (sin acceso completo, usados como guía de estructura).

---

## PT-01 – Elevar cobertura > 92% en núcleo

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (exacto de la consigna del usuario): “Tengo un 89% de covertura... necesito que sea mayor a 92%”.
- Instrucciones del sistema: Escribir pruebas unitarias mínimas y específicas; mantener `.coveragerc` para medir únicamente `core/` como métrica central.
- Respuesta/Resultado: Se añadieron/ajustaron tests para rutas de error y casos límite en `core/` y CLI; la cobertura central subió a ~96% (ver `Report.md`).
- Uso: Aplicado sin cambios.
- Archivos finales:
	- `test/test_backgm.py`
	- `test/test_tablero.py`
	- `test/test_jugador.py`
	- `test/test_dice.py`
	- `test/test_cli.py`
	- `.coveragerc`

---

## PT-02 – Incorporar pruebas de CLI en un único archivo

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (exacto de la consigna del usuario): “agrega esos test al archivo de test_cli.py”.
- Instrucciones del sistema: Consolidar casos de CLI (ayuda, opciones inválidas, fin de entrada) y usar `unittest` con mocking de `input/print` cuando corresponda.
- Respuesta/Resultado: Los tests de CLI fueron integrados en `test/test_cli.py`, cubriendo validaciones e interacción básica.
- Uso: Aplicado.
- Archivos finales:
	- `test/test_cli.py`

---

## PT-03 – Configurar medición de cobertura con exclusiones

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (resumen): “Ajustar `.coveragerc` para omitir `cli/` y `pygame_ui/` al medir cobertura de núcleo.”
- Instrucciones del sistema: Mantener exclusiones estándar (venv, __pycache__, test) y añadir rutas de UI/CLI.
- Respuesta/Resultado: `.coveragerc` actualizado con omits para `cli/*` y `pygame_ui/*` además de carpetas transitorias.
- Uso: Aplicado.
- Archivos finales:
	- `.coveragerc`

---

## PT-04 – Caso borde (barra bloqueada) y pérdida de turno

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (exacto de la consigna del usuario): “... con ficha en barra ... puntos bloqueados ... debe perder el turno ... arregles eso”.
- Instrucciones del sistema: Implementar en UI sin romper `core/`. Proponer pruebas si es viable.
- Respuesta/Resultado: La lógica se implementó en `pygame_ui/game_ui.py` (no en `core/`), por lo que no se agregaron tests unitarios directos en `core`; se sugiere como mejora futura un test de integración/UI headless o migrar parte de la decisión a `core` para hacerla testeable sin gráfica.
- Uso: Aplicado (en UI); pruebas descartadas por alcance de interfaz gráfica en esta iteración.
- Archivos finales:
	- `pygame_ui/game_ui.py`

---

## PT-05 – Verificación de pipeline de pruebas en CI

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (resumen): “Configurar CI para correr unittest + coverage y publicar artefactos de resultados.”
- Instrucciones del sistema: Usar Ubuntu, Python 3.10, `coverage` y `unittest`.
- Respuesta/Resultado: Workflow `ci.yml` ejecuta `coverage run -m unittest`, genera `coverage xml` y `coverage_report.txt`, publica artefactos y comenta en PR.
- Uso: Aplicado.
- Archivos finales:
	- `.github/workflows/ci.yml`
	- `coverage_report.txt` (artefacto)
	- `cobertura.xml` (artefacto)

	---

	### Referencias externas
	- Chats IA compartidos por el usuario (posible autenticación requerida):
		- ChatGPT: https://chatgpt.com/share/69068e1d-ac4c-8011-838a-98ae9bfed681
		- Gemini: https://gemini.google.com/share/40163a1c1595, https://gemini.google.com/share/b66d3ec7f154
