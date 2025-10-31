Backgammon en Python (CLI + Pygame)
===================================

Autor: Luciano Panella

Introducción
------------
Proyecto final de Backgammon con doble interfaz: línea de comandos (CLI) y Pygame (GUI). La lógica del juego está completamente desacoplada de las interfaces, se aplican principios SOLID, y se acompaña con una suite de tests con cobertura superior al 90%.

Estructura del proyecto
-----------------------
- `core/` — Lógica de dominio (Backgammon, Tablero, Jugador, Dados, Excepciones). Responsabilidad única: reglas del juego y estado.
- `cli/` — Interfaz de consola. Responsabilidad única: entrada/salida por texto y validación de usuario.
- `pygame_ui/` — Interfaz gráfica con Pygame. Responsabilidad única: dibujo del tablero, manejo de eventos y orquestación visual.
- `test/` — Pruebas unitarias de dominio y CLI.
- `assets/` — Recursos opcionales (imágenes/sonidos) si aplica.

Esta separación garantiza el desacoplamiento entre Lógica/Core y las Interfaces, permitiendo evolucionar la UI sin tocar el dominio.

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

Ejecución de tests y cobertura
------------------------------
```powershell
& .\\venv\\Scripts\\Activate.ps1
coverage run -m unittest -v
coverage report -m
```
Meta de cobertura: 90%+. El proyecto alcanza ~94% en los últimos reportes.

Notas y troubleshooting
-----------------------
- Para ocultar el banner de Pygame en consola, se puede usar `PYGAME_HIDE_SUPPORT_PROMPT=1`.
- Si PowerShell bloquea scripts: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` (solo para la sesión actual si es necesario).
- Si la UI no abre, verificá que `pygame` esté instalado y que el entorno virtual esté activado.

Licencia
--------
Uso académico.
