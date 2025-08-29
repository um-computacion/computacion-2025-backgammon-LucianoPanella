# Consigna Proyecto Backgammon

## Resumen

El objetivo de este documento es guiar el desarrollo de un juego de Backgammon en Python, siguiendo las reglas y mecánicas tradicionales. El juego permitirá partidas tanto en consola como en una interfaz gráfica con Pygame.

- Jugar online: [Ludoteka Backgammon](https://www.ludoteka.com/clasika/backgammon-es.html)

---

## 1. Introducción

El desarrollo se realizará en Python, primero en línea de comando y luego con interfaz gráfica usando Pygame. La lógica del juego estará separada de la presentación.

---

## 2. Requisitos del Juego

### 2.1. Tablero de juego

- 24 triángulos (puntos), divididos en 4 cuadrantes.
- Cada jugador comienza con 15 fichas en posiciones estándar.

### 2.2. Fichas y dados

- Cada jugador tiene 15 fichas.
- Se usan dos dados de seis caras.
- Tiradas dobles permiten repetir los valores.

### 2.3. Jugabilidad

- Movimientos válidos, capturas y reingresos desde la barra.
- Implementar condición de victoria.

---

## 3. Diseño del Juego

### 3.1. Lógica Central (`core/`)

- Clases separadas para Game, Board, Dice y Player.
- Lógica independiente de la interfaz.

### 3.2. Modalidades de Interfaz

#### 3.2.1. Línea de Comando (Obligatorio)

- Interacción por comandos de texto.
- Colocar piezas, intercambios y puntuación por consola.

#### 3.2.2. Gráficos con Pygame (Obligatorio)

- Interfaz gráfica con Pygame.
- Representación visual del tablero y fichas.
- Interacción con ratón y teclado.
- La lógica es la misma que en la CLI.

### 3.3. Guardado de Partidas en Redis (Opcional)

- Sistema de guardado usando Redis.
- Permite reanudar partidas desde el punto exacto.

### 3.4. Estructura del Proyecto

```
/backgammon/
├── core/           → lógica del juego
├── cli/            → CLI
├── pygame_ui/      → interfaz gráfica
├── assets/         → imágenes, sonidos
└── requirements.txt
```

---

## 4. Desarrollo y Buenas Prácticas

### 4.1. Cobertura del Código

- Al menos 90% de cobertura con pruebas unitarias para la lógica central.

### 4.2. Desarrollo Incremental

- Avances quincenales.
- Entregas y commits distribuidos en el tiempo.

### 4.3. Documentación y Calidad

- Docstrings obligatorios.
- README.md y CHANGELOG.md.
- Seguir principios SOLID.

### 4.4. Integración Continua y Control de Calidad

- CI con CircleCI o Travis.
- Pruebas unitarias automáticas en cada commit.
- Uso de CodeClimate o coveralls.io para cobertura.
- Calificación CodeClimate: A y 0 issues al final.

### 4.5. Inclusión de Prompts

- Archivos obligatorios:  
  - prompts-desarrollo.md  
  - prompts-testing.md  
  - prompts-documentacion.md  
- Por cada prompt:  
  - Modelo/herramienta usada.
  - Texto exacto del prompt.
  - Instrucciones del sistema (si hubo).
  - Respuesta/resultado completo.
  - Indicar uso (sin cambios, con modificaciones, descartada).
  - Referencia a archivos finales.

### 4.6. Justificación escrita (Markdown)

- Archivo obligatorio: JUSTIFICACION.md
- Contenido mínimo:
  - Resumen del diseño general.
  - Justificación de clases y atributos.
  - Decisiones de diseño.
  - Excepciones y manejo de errores.
  - Estrategias de testing y cobertura.
  - Referencias a SOLID.
  - Anexos: diagramas UML.
- Debe actualizarse a lo largo del cursado.

### 4.7. Justificación oral

- Exposición general del proyecto.
- Decisiones de diseño.
- Estrategia de testing y evidencia.
- Implementación concreta.
- Evaluación de la comprensión.

---

## 5. Diseño Básico Propuesto

### 5.1. Clases

- **BackgammonGame**: Coordina flujo general.
- **Board**: Representa el tablero y puntos.
- **Player**: Representa a un jugador.
- **Dice**: Lógica de tiradas.
- **Checker**: Representa cada ficha.
- **CLI**: Interfaz de texto.
- **PygameUI**: Interfaz gráfica.

### 5.2. Relaciones

```
BackgammonGame
├─ Board
├─ Player
├─ Dice
└─ Interfaces: CLI / PygameUI
```

---

## 6. Aprobación de la materia

- Cumplimiento de todas las features antes del fin del semestre.
- Sprints de 14 días, mínimo 10 commits por sprint.
- CHANGELOG.md obligatorio.
- Principios SOLID en todo el código.
- Atributos con prefijo y postfijo "__".
- Documentación con docstrings.
- README.md con instrucciones para testing y juego (incluyendo Docker).
- Trabajo individual.
- Commits reflejan evolución progresiva.
- Versión final en branch MAIN, con protección contra push directo.
- CodeClimate: A y 0 issues.

### 6.1. Sospecha de copia y trazabilidad

- Se considerará copia si hay similitud notable.
- El commit más reciente es el que copió.
- Mantener historial de commits y archivos de prompts y justificación.

---

## 7. Referencias

- [Wikipedia Backgammon](https://es.wikipedia.org/wiki/Backgammon)
- [Pygame Docs](https://www.pygame.org/docs/)
- [Real Python: Documenting Python Code](https://realpython.com/documenting-python-code/)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)