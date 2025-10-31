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

