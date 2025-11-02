Backgammon en Python (CLI + Pygame)
===================================

Autor: Luciano Panella

Descripción
-----------
Proyecto final de Backgammon con doble interfaz: línea de comandos (CLI) y Pygame (GUI). La lógica del juego está desacoplada de las interfaces (principios SOLID), con suite de tests y cobertura central > 90%.

Tabla de contenidos
-------------------
- Descripción (este apartado)
- Características clave
- Estructura del proyecto
- Instalación y prerrequisitos (Windows PowerShell)
- Guía de ejecución (CLI y GUI)
- Controles (GUI)
- Diagrama de clases (imagen)
- Ejecución de tests y cobertura
- Notas y troubleshooting
- Licencia

Características clave
---------------------
- Lógica de dominio independiente de las UIs (CLI y Pygame)
- Reglas completas de backgammon: barra, reingreso, bloqueos, home y “bear off”
- Regla de calidad de vida en GUI: pasa turno automáticamente si no hay movimientos válidos (incluye bloqueo desde barra)
- Suite de pruebas unitarias con cobertura central ~96% (según Report.md)
- Pipeline de CI: tests + coverage + Pylint y publicación de artefactos

Estructura del proyecto
-----------------------
- `core/` — Lógica de dominio (Backgammon, Tablero, Jugador, Dados, Excepciones)
- `cli/` — Interfaz de consola (entrada/salida por texto y validación)
- `pygame_ui/` — Interfaz gráfica (dibujo, eventos, orquestación visual)
- `test/` — Pruebas unitarias de dominio y CLI
- `assets/` — Recursos opcionales (imágenes/sonidos)

Esta separación garantiza el desacoplamiento entre dominio e interfaces, permitiendo evolucionar la UI sin tocar el core.

Instalación y prerrequisitos
----------------------------
Requisitos: Python 3.11+ en Windows/Linux/macOS.

1) Crear y activar un entorno virtual (Windows PowerShell):
```powershell
cd "C:\\Users\\lucia\\Documents\\Universidad\\Año N°2\\Computación\\Segundo Semestre\\Proyecto Final\\computacion-2025-backgammon-LucianoPanella"
python -m venv venv
& .\\venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
```

2) Instalar dependencias:
```powershell
pip install -r requirements.txt
```
Si no contás con `requirements.txt`, instalá al menos Pygame para la GUI:
```powershell
pip install pygame
```

Guía de ejecución
-----------------
Modo CLI (consola):
```powershell
& .\\venv\\Scripts\\Activate.ps1
python -m cli.cli
```

Modo Pygame (GUI):
```powershell
& .\\venv\\Scripts\\Activate.ps1
python -m pygame_ui.main_pygame
```
- La GUI muestra primero una pantalla para ingresar los nombres y luego abre el tablero.

Alternativa (GUI con nombres por consola):
```powershell
& .\\venv\\Scripts\\Activate.ps1
python -m pygame_ui.game_ui
```
- En este modo, los nombres se ingresan en la consola y, luego, se inicia la ventana gráfica.

Controles (GUI)
---------------
- Espacio: tirar dados
- Click izquierdo: seleccionar origen (o "barra")
- Click derecho: mover al destino resaltado / reingresar / sacar ficha
- Overlay final: Reiniciar o Finalizar

Diagrama de clases
------------------
El diagrama resume el modelo de dominio (core) y las interfaces (CLI/Pygame); se presenta en ASCII legible:

```text
                                                                ┌───────────────────────────┐
                                                                │        Backgammon         │  (orquestador)
                                                                ├───────────────────────────┤
                                                                │ - tablero: Tablero        │
                                                                │ - jugador1, jugador2      │
                                                                │ - dados: Dice             │
                                                                ├───────────────────────────┤
                                                                │ + iniciar_partida()       │
                                                                │ + tirar_dados()           │
                                                                │ + mover_ficha()           │
                                                                │ + cambiar_turno()         │
                                                                │ + verificar_ganador()     │
                                                                └──────────┬────────────────┘
                                                                                                         │ usa/coordina
                                ┌──────────────────┼──────────────────┐
                                │                  │                  │
                                ▼                  ▼                  ▼
        ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
        │   Jugador     │  │   Tablero     │  │     Dice      │
        ├───────────────┤  ├───────────────┤  ├───────────────┤
        │ + nombre:str  │  │ + puntos[24]  │  │ + tirar()     │
        │ + color:str   │  │ + barra:{b,n} │  │ + valores[]   │
        │ + fuera:int   │  │ + fuera:{b,n} │  │ + usar_valor()│
        └───────────────┘  └───────────────┘  └───────────────┘

                                         ┌─────────────┐                    ┌────────────────┐
                                         │     CLI     │                    │   Pygame UI    │
                                         ├─────────────┤                    ├────────────────┤
                                         │ input/print │                    │ render/eventos │
                                         └──────┬──────┘                    └───────┬────────┘
                                                                        │                                 │
                                                                        └──────────► usa Backgammon ◄─────┘

Excepciones de dominio (ejemplos): OrigenSinFicha, DestinoBloqueado,
NoPuedeReingresar, NoPuedeSacarFicha, TurnoIncorrecto, JuegoYaTerminado.
```

Ejecución de tests y cobertura
------------------------------
```powershell
& .\\venv\\Scripts\\Activate.ps1
coverage run -m unittest -v
coverage report -m
```
Meta de cobertura: 90%+. El proyecto alcanza ≈94–96% en los últimos reportes.

Notas y troubleshooting
-----------------------
- Para ocultar el banner de Pygame en consola, se puede usar `PYGAME_HIDE_SUPPORT_PROMPT=1`.
      │ + procesar_comando()      │                     │ + manejar_eventos()        │
      └─────────────┬─────────────┘                     └──────────────┬────────────┘
                    │                                               │
                    │ llama                                          │ llama
                    │                                               │
                    └──────────────────────► BackGammon ◄────────────┘
