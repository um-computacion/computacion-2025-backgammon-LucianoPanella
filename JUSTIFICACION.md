# JUSTIFICACION.md — Diseño y Calidad

Autor: Luciano Panella

Resumen
-------
Este documento describe las decisiones de diseño, arquitectura, manejo de errores y estrategia de pruebas del proyecto Backgammon. El foco es mantener un fuerte desacoplamiento entre la lógica del juego (core) y las interfaces (CLI/GUI), aplicando principios SOLID y buenas prácticas de ingeniería.

Diseño general y arquitectura
----------------------------
- Separación estricta por responsabilidades:
	- `core/`: dominio puro del juego. Define reglas, estado y excepciones de dominio. No depende de ninguna UI.
	- `cli/`: orquesta la interacción por consola (inputs/prints), valida entradas y traduce mensajes; delega reglas al `core`.
	- `pygame_ui/`: renderiza el tablero, recoge eventos de teclado/mouse y actualiza la UI; delega la lógica del juego al `core`.

- Inyección de dependencias (DIP) en `core/backgammon.py`:
	- El constructor de `Backgammon` acepta instancias inyectadas para tablero, dados y jugadores (`tablero_inst`, `dados_inst`, `jugador1_inst`, `jugador2_inst`).
	- Beneficios: pruebas unitarias más sencillas, bajo acoplamiento, posibilidad de sustituir implementaciones sin cambiar el orquestador del juego.

- Mapeo de clases (core/):
	- `Backgammon`: orquestador del flujo del juego (tira dados, cambia turno, coordina movimientos y condición de victoria). No conoce nada de entrada/salida.
	- `tablero`: estado y reglas de tablero (validación de movimientos, comer/reingresar, home, sacar ficha fuera, barra).
	- `jugador`: encapsula el estado del jugador (nombre, color, fichas restantes) y sus operaciones (sacar ficha a afuera, detectar victoria).
	- `dice`: encapsula tiradas, dobles y estado de última tirada.
	- `excepciones`: tipifica errores de dominio (e.g., `DestinoBloqueado`, `NoPuedeReingresar`, `NoPuedeSacarFicha`, `TurnoIncorrecto`, `JuegoYaTerminado`, etc.).

Principios SOLID en el código
-----------------------------
- SRP (Responsabilidad Única):
	- `tablero` gestiona únicamente el estado del tablero y sus reglas; `Backgammon` coordina el flujo de alto nivel; `jugador` administra fichas/restantes; `dice` maneja dados.
	- Las UIs (CLI / Pygame) solo se encargan de interacción y visualización.

- OCP (Abierto/Cerrado):
	- Se pueden agregar nuevas interfaces (por ejemplo, una REST API) sin modificar `core/`.
	- La lógica del juego permanece estable; las extensiones ocurren en capas externas.

- LSP (Sustitución de Liskov):
	- Aunque no se usan jerarquías complejas, los puntos de extensión (instancias inyectables) respetan expectativas de comportamiento, permitiendo sustituciones seguras en pruebas o prototipos.

- ISP (Segregación de Interfaces):
	- Cada módulo expone una superficie mínima (métodos necesarios) y evita interfaces "gordas"; las UIs consumen solo lo que necesitan.

- DIP (Inversión de Dependencias):
	- `Backgammon` depende de abstracciones (contratos implícitos) y acepta instancias por parámetro en su constructor, en lugar de construirlas rígidamente.

Manejo de errores y excepciones
-------------------------------
- Motivo: las reglas del dominio se expresan con claridad mediante excepciones específicas, en lugar de múltiples if/else anidados.
- Ejemplos: `DestinoBloqueado`, `OrigenSinFicha`, `NoPuedeReingresar`, `NoPuedeSacarFicha`, `TurnoIncorrecto`, `JuegoYaTerminado`.
- Beneficios: flujos de control más legibles, tests más precisos, y responsabilidades bien divididas entre dominio e interfaz.

Estrategia de testing y cobertura
---------------------------------
- Objetivo de cobertura: > 90% (cumplido en el proyecto; reportes típicos ~94%).
- Tipos de pruebas:
	- Unitarias de `core/`: validan reglas de tablero, tiradas de dados (incluye dobles), flujo de Backgammon (cambio de turno, fin de juego, reingreso, sacar ficha), y estado de jugadores.
	- Unitarias de `cli/` con mocking: simulan entradas del usuario, validan mensajes y manejo de errores, y aseguran que el loop no queda bloqueado ante fin de input.
- Herramientas: `unittest` + `coverage`.
- Ejecución típica:
	```powershell
	& .\\venv\\Scripts\\Activate.ps1
	coverage run -m unittest -v
	coverage report -m
	```

Anexos y mejoras futuras
------------------------
- Anexos sugeridos: diagramas UML (clases y flujo) para documentación complementaria.
- Mejoras:
	- Tests de humo para Pygame (validar arranque y eventos básicos).
	- `requirements.txt` y/o `pyproject.toml` para empaquetado formal.
	- Docker opcional para estandarizar ejecución.
	- Persistencia opcional (e.g., Redis) para guardar/cargar partidas.

Contratos del dominio (mini-ESPEC)
----------------------------------
- Entradas principales:
	- Tirar dados: sin parámetros; salida: lista ordenada de valores disponibles (dobles duplican movimientos).
	- Mover ficha: (jugador, origen -> destino) o (reingreso desde barra -> punto). Salida: estado válido o excepción de dominio.
	- Cambio de turno: implícito al consumir todos los valores de dados o cuando no hay movimientos válidos.
- Invariantes clave:
	- Un jugador con fichas en barra debe reingresar antes de cualquier otro movimiento.
	- Un punto con 2+ fichas del rival está bloqueado; solo puede ocuparlo el propietario o golpear si hay exactamente 1 ficha rival.
	- “Bear off” solo desde el home cuando todas las fichas propias están en el cuadrante final.
- Criterios de éxito por jugada:
	- El movimiento consume exactamente un valor de dado disponible.
	- No viola bloqueos ni reglas de reingreso/bear off.
	- Actualiza correctamente barra, capturas y conteos de “fichas_fuera”.

Estados y flujos esenciales
---------------------------
- Barra y reingreso: si los puntos de entrada (según dado) están bloqueados, el jugador no puede moverse. En la GUI se aplica “auto-pass” del turno tras tirar y verificar ausencia de movimientos válidos.
- Dobles: duplican la cantidad de movimientos (4 valores idénticos). El consumo se lleva en `dice`.
- Golpe y envío a barra: si el destino tiene exactamente 1 ficha rival, se captura y se envía a la barra del contrario.
- Fin de juego: cuando un jugador coloca todas sus fichas “fuera”, `Backgammon` detiene el juego y reporta ganador.

Excepciones mapeadas a reglas
-----------------------------
- `NoPuedeReingresar`: hay fichas en barra y no existen puntos de entrada libres según los dados.
- `DestinoBloqueado`: el destino tiene 2+ fichas rivales.
- `OrigenSinFicha`: el punto de origen no contiene ficha del jugador activo.
- `NoPuedeSacarFicha`: intento de “bear off” fuera de condiciones (piezas fuera del home o distancia inválida).
- `TurnoIncorrecto`: acciones intentando mover con el jugador opuesto al activo.
- `JuegoYaTerminado`: cualquier acción posterior a la condición de victoria.

Decisiones y trade-offs
-----------------------
- “Auto-pass” en GUI: mejora UX; se implementa solo en la capa de interfaz para no acoplar el core a decisiones de presentación. El core conserva el contrato puro de reglas.
- Inyección de dependencias sencilla (sin framework): suficiente para pruebas y facilita reemplazos en el futuro.
- CLI mínima: mantiene el foco en validación y mensajes; no se mezcla la lógica con el rendering.

Mantenibilidad y extensibilidad
-------------------------------
- Nuevas UIs (por ejemplo, una API REST o una app móvil) pueden reutilizar `core/` sin cambios.
- Reglas adicionales o variantes (e.g., backgammon con dobles cancelables) pueden aislarse en nuevas implementaciones de `dice` o extensiones en `tablero` sin alterar la CLI/GUI.
- Los nombres y métodos públicos de `core/` actúan como contrato estable; se documentan en README y en tests.

Calidad: lint, CI y puertas de control
--------------------------------------
- Linting: Pylint con configuración dedicada; puntuación mejorada durante el proyecto.
- CI: ejecución automática de tests, cobertura (XML y reporte de texto) y Pylint; publicación de artefactos y comentario en PRs.
- Puertas de calidad (estado actual):
	- Build: PASS (módulos compilan y tests inician)
	- Lint/Typecheck: PASS (advertencias controladas en Pylint)
	- Tests: PASS (suite unitaria OK)
	- Cobertura central: PASS (≈94–96% en `core/` según Report.md)

Diagrama de clases (referencia)
--------------------------------
El diagrama actualizado vive en el README en formato ASCII legible (sección “Diagrama de clases”).

Notas de interpretación:
- El módulo `Backgammon` orquesta a `Tablero`, `Jugador` y `Dice`.
- `CLI` y `PygameUI` son clientes del dominio: no contienen lógica de reglas.
- Las excepciones modelan fallas de dominio y son consumidas por las UIs para mensajes/flujo.

