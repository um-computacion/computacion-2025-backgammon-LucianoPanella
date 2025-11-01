## Registro de Prompts de IA — Documentación

Este documento lista los prompts utilizados para producir y mantener la documentación del proyecto. Por cada entrada: modelo/herramienta, instrucciones del sistema (si existieron), prompt exacto, respuesta/resultado, uso (tal cual/modificada/descartada) y archivos vinculados.

Como guía de estilo se consideraron únicamente enlaces a chats externos compartidos por el usuario.

---

## PDOC-01 – Actualizar reporte de cobertura (`Report.md`)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (exacto de la consigna del usuario): “actualices el archivo de Report.md”.
- Instrucciones del sistema: Mantener formato claro, incluir tabla de `coverage report -m` y mencionar el `.coveragerc` aplicado.
- Respuesta/Resultado: Se actualizó `Report.md` con el resumen de cobertura del núcleo (96%) y los archivos con líneas faltantes. Se explicitó que `cli/` y `pygame_ui/` quedan omitidos para el cálculo central.
- Uso: Aplicado sin cambios relevantes.
- Archivos finales:
	- `Report.md`
	- `.coveragerc`

---

## PDOC-02 – Documentación automática en CI (REPORTS.md + comentario en PR)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (resumen): “Necesito agregar esto [CI YAML]... Realizalo: correr tests con coverage, Pylint, subir artefactos y comentar en PR.”
- Instrucciones del sistema: Mantener el pipeline simple (Ubuntu), usar `coverage` y `pylint` con `.pylintrc`; generar un `REPORTS.md` agregando cobertura y pylint.
- Respuesta/Resultado: Se añadió `.github/workflows/ci.yml` que ejecuta tests+coverage, genera `cobertura.xml` y `coverage_report.txt`, corre Pylint contra `core cli pygame_ui`, produce `REPORTS.md` y sube artefactos. En PRs, comenta el resumen de cobertura.
- Uso: Aplicado con modificaciones menores (nombres y rutas).
- Archivos finales:
	- `.github/workflows/ci.yml`
	- `REPORTS.md` (generado por CI)

---

## PDOC-03 – Justificación técnica (revisión)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (resumen): “Verificá que JUSTIFICACION.md cubra diseño, SOLID, manejo de errores y estrategia de testing; ajustá si falta.”
- Instrucciones del sistema: No introducir cambios invasivos; priorizar claridad y alineación a la consigna.
- Respuesta/Resultado: Contenido validado; describe arquitectura, SOLID, excepciones, y ejecución de pruebas con cobertura; se agregaron notas menores cuando fue necesario.
- Uso: Aplicado con modificaciones menores/validado.
- Archivos finales:
	- `JUSTIFICACION.md`

---

## PDOC-04 – README: guía de uso (CLI + Pygame) y tests (revisión)

- Herramienta/Modelo: Asistente en VS Code (copilot/LLM).
- Prompt (resumen): “Asegurá que el README tenga pasos en Windows PowerShell para entorno virtual, instalación, ejecución de CLI y GUI, y correr coverage.”
- Instrucciones del sistema: Mantener ejemplos listos para copiar en PowerShell; incluir activar venv y comandos `python -m ...`.
- Respuesta/Resultado: Se verificó que `README.md` ya contenía los pasos completos para Windows (PowerShell), la ejecución de CLI/GUI y la sección de coverage; no se requirieron cambios sustanciales.
- Uso: Validado (sin cambios).
- Archivos finales:
	- `README.md`

---

### Referencias externas
- Chats IA compartidos:
	- ChatGPT: https://chatgpt.com/share/69068e1d-ac4c-8011-838a-98ae9bfed681
	- Gemini: https://gemini.google.com/share/40163a1c1595, https://gemini.google.com/share/b66d3ec7f154
	Nota: acceso completo restringido; se tomaron como referencia de estructura.
