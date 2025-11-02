# Registro de Cambios

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

**Nota**: Este registro está organizado cronológicamente (más antiguo primero) para mostrar la evolución del proyecto a lo largo del tiempo.

## [Sin Publicar]

## [0.1.0] - 2025-08-28

### Agregado
- Estructura inicial del proyecto con directorios principales
- Documentación del proyecto con requisitos del juego (`CONSIGNA.md`)
- Clase `Pieza` para el manejo de fichas del juego
- Fundación básica de la clase `Tablero`
- Base para el desarrollo del juego de backgammon
- Directorios principales: `core/`, `cli/`, `test/`, `assets/`

### Infraestructura
- Configuración del repositorio GitHub
- Esqueleto básico del proyecto

## [0.2.0] - 2025-09-09

### Agregado
- Clase `Tablero` mejorada con manejo de posiciones
- Lógica básica del tablero de juego y validación de movimientos
- Cobertura de pruebas para funcionalidad del tablero
- Integración de jugadores con el manejo del tablero

### Cambiado
- Diseño mejorado de la clase tablero y lógica del juego

## [0.3.0] - 2025-09-10

### Agregado
- Clase `Jugador` mejorada con manejo de fichas
- Seguimiento del estado del jugador e interacción del juego
- Cobertura completa de pruebas para funcionalidad del jugador
- Métodos de control y manejo de fichas del jugador

### Cambiado
- Diseño y funcionalidad mejorada de la clase jugador

## [0.4.0] - 2025-09-11

### Agregado
- Clase controladora principal `Backgammon`
- Manejo del estado del juego y gestión de turnos
- Integración entre todos los componentes principales
- Suite completa de pruebas para la clase Backgammon

### Cambiado
- Lógica del juego mejorada con manejo adecuado del estado
- Interacciones y dependencias de clases mejoradas

## [0.5.0] - 2025-09-23

### Agregado
- Funcionalidad mejorada del tablero con nuevos métodos (barra, reingreso, home, sacar ficha fuera)
- Características adicionales de lógica del juego en la clase tablero
- Cobertura completa de pruebas para las nuevas características del tablero

### Cambiado
- Clase tablero mejorada con funcionalidad extendida
- Mejor seguimiento y manejo del estado del juego

## [1.0.0] - 2025-09-11

### Agregado
- Implementación completa de la lógica principal del juego
- Clases principales del juego: `Backgammon`, `Jugador`, `Tablero`, `Pieza`, `Dice`
- Implementación completa de las reglas del backgammon
- Suite completa de pruebas para toda la funcionalidad principal
- Manejo de jugadores con seguimiento de fichas
- Manejo del estado del tablero con 24 posiciones
- Lanzamiento de dados con manejo de dobles
- Detección de condiciones de victoria

### Cambiado
- Arquitectura principal del juego finalizada
- API estable establecida para componentes del juego

## [1.1.0] - 2025-09-23

### Agregado
- Primera versión del archivo CHANGELOG.md
- Funcionalidad mejorada del tablero con nuevos métodos
- Características adicionales de lógica del juego en la clase tablero
- Cobertura completa de pruebas para nuevas características

### Cambiado
- Clase tablero mejorada con funcionalidad extendida
- Mejor seguimiento y manejo del estado del juego

## [1.2.0] - 2025-09-25

### Agregado
- Implementación completa de CLI para interacción del juego
- Controlador principal del juego (`core/backgammon.py`)
- Manejo del estado del juego y gestión de turnos
- Integración entre todos los componentes principales

### Cambiado
- Lógica del juego mejorada con manejo adecuado del estado
- Interacciones y dependencias de clases mejoradas

## [1.3.0] - 2025-09-28

### Agregado
- Interfaz CLI mejorada con indicadores de turno
- Visualización de información de uso de dados
- Mejor guía para el usuario en acciones del juego
- Visualización mejorada del flujo del juego

### Corregido
- Implementaciones de pruebas corregidas para mejor confiabilidad
- Cobertura de código mejorada a través de pruebas comprensivas
- Corregidos problemas de nomenclatura de variables y consistencia

## [1.4.0] - 2025-09-29

### Agregado
- Sistema completo de manejo de excepciones con excepciones personalizadas
- Captura y manejo de errores en la interfaz CLI
- Manejo robusto de errores a lo largo del código
- Clases de excepciones personalizadas en `core/excepciones.py`

### Cambiado
- Interfaz CLI mejorada con mejores mensajes de error
- Estabilidad del juego mejorada con manejo adecuado de excepciones

## [1.5.0] - 2025-09-30

### Agregado
- Suite completa de pruebas alcanzando 96% de cobertura de código
- Representación visual del tablero CLI con arte ASCII
- Experiencia de usuario mejorada en la interfaz de línea de comandos
- Casos de prueba adicionales para todas las clases principales del juego

### Corregido
- Confiabilidad de pruebas mejorada y métricas de cobertura
- Mejor retroalimentación visual en modo CLI

## [2.0.0] - 2025-10-12

### Agregado
- Implementación completa de GUI en Pygame con interfaz gráfica
- Clase principal de UI del juego (`game_ui.py`) para manejo completo del juego
- Sistema de manejo de eventos para interacciones de mouse y teclado
- Renderizador visual de dados con efectos de animación de rodamiento
- Renderizador interactivo del tablero con posiciones clickeables
- Módulo de constantes con colores, dimensiones y fuentes estandarizadas
- Estructura completa de UI en pygame en el directorio `pygame_ui/`

### Cambiado
- Estructura del proyecto mejorada para soportar interfaces CLI y GUI
- Arquitectura del juego mejorada para soportar múltiples tipos de interfaz

## [2.1.0] - 2025-11-01

### Agregado
- Regla en la UI: pasar turno automáticamente cuando hay fichas en barra y los puntos de reingreso están bloqueados con las tiradas actuales, o cuando no existen movimientos posibles tras tirar.
- Archivos de prompts completos según consigna: `promts/prompts-desarrollo.md`, `promts/prompts-documentacion.md`, `promts/prompts-testing.md`.

### Cambiado
- `pygame_ui/game_ui.py`: normalización de indentación/estructura y mejora de mensajes de estado para guiar acciones (tirar dados, seleccionar/mover, pase de turno automático).
- `pygame_ui/main_pygame.py`: limpieza del bloque principal y llamada a `GameUI.run()`.

### Corregido
- Error de ejecución al iniciar la GUI (falta de método `run` en `GameUI`) solucionado agregando `GameUI.run()` y ajustando llamadas.
- Correcciones menores en núcleo para estabilidad y lint: dedent en retorno de `core/backgammon.py`; `__str__` en `core/jugador.py`; normalización de `reiniciar_turno` y naming en `core/dice.py`; limpieza en `core/excepciones.py`.
- Compilación limpia de módulos `pygame_ui/` y eliminación de mezclas tabs/espacios.

### Infraestructura
- CI con GitHub Actions: ejecución de tests con coverage, análisis con Pylint y publicación de artefactos (coverage XML, reporte de coverage y Pylint), más comentario automático de cobertura en PRs (`.github/workflows/ci.yml`).

### Documentación
- `Report.md` actualizado con cobertura del núcleo (~96%) usando `.coveragerc` para excluir `cli/` y `pygame_ui/` del cálculo central.
- README verificado con instrucciones para Windows PowerShell (venv, instalación, ejecución CLI/GUI, coverage).

---

## Guías de Formato

Este registro de cambios sigue el formato de [Keep a Changelog](https://keepachangelog.com/en/1.0.0/):

- **Agregado** para nuevas características
- **Cambiado** para cambios en funcionalidad existente
- **Obsoleto** para características que pronto serán removidas
- **Removido** para características ya removidas
- **Corregido** para corrección de errores
- **Seguridad** para correcciones de vulnerabilidades

## Resumen del Historial de Versiones (Evolución Cronológica)

- **v0.1.0**: Fundación del proyecto
- **v0.2.0**: Fundación de la lógica del tablero
- **v0.3.0**: Sistema de manejo de jugadores
- **v0.4.0**: Implementación del controlador Backgammon
- **v0.5.0**: Desarrollo de fichas y tablero del juego
- **v1.0.0**: Finalización de la lógica principal del juego
- **v1.1.0**: Funcionalidad mejorada del tablero
- **v1.2.0**: Implementación completa de CLI
- **v1.3.0**: Interfaz CLI mejorada
- **v1.4.0**: Sistema de manejo de excepciones
- **v1.5.0**: Pruebas comprensivas y CLI visual
- **v2.0.0**: Implementación completa de GUI en Pygame

## Enlaces

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Versionado Semántico](https://semver.org/spec/v2.0.0.html)
- Las fechas y versiones corresponden a los commits principales de tu historial.
- Para cada nueva versión, agrega la fecha y los cambios realizados.