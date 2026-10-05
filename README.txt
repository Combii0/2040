ROBOYORK 2040
README
==============================

AUTOR / AUTHOR
Santiago Hernández Sotomonte
Colegio Anglo Americano - 11E

GitHub:
https://github.com/Combii0

Repositorio / Repository:
https://github.com/Combii0/2040


ESPAÑOL
––––––––

1. DESCRIPCIÓN

RoboYork 2040 es un sistema interactivo, a modo de videojuego, de gestión de emergencias desarrollado
en Python con Tkintery Random. El proyecto simula una central de control en la que un
operador debe administrar recursos, responder eventos, tomar decisiones,
controlar daños y mantener una misión operativa.

Fue desarrollado como proyecto individual para RoboYork VII.


2. TECNOLOGÍAS

- Python 3, 64-bit
- Tkinter / ttk
- pygame para música y efectos de sonido
- random para eventos, movimiento y variación de la simulación
- JSON para persistencia de datos y backups
- ctypes para registro de fuentes en sistemas compatibles
- Fuentes Pixeloid incluidas localmente


3. ESTRUCTURA PRINCIPAL

- main.py
  Interfaz gráfica, navegación, misión, Damage Pad, audio, estadísticas,
  simulación, backups y reportes.

- events.py
  Eventos, acciones, efectos, dificultad y puntajes.

- resources.py
  Gestión de Energy, Water, Food y Communication.

- missions.py
  Carga y guardado de misiones en .data/missions.json.

- users.py
  Validación de usuarios base.

- .data/
  missions.json y operators.json.

- Backups/
  Backups exportados por el usuario.

- Resources/
  Fuentes, música, GIF visual, iconos y efectos de sonido.

- Resources/SFX/
  sl.mp3, damage.mp3, pop.mp3 y start.mp3.

- Resources/icons/
  logo.png y volume.png.


4. FUNCIONALIDADES PRINCIPALES

- Login y creación de operadores.
- Creación de misiones con dificultad Easy, Medium o Hard.
- Recursos iniciales:
  Energy 100, Water 80, Food 110, Communication 90.
- Cinco tipos de eventos de emergencia.
- Decisiones con consecuencias sobre recursos y puntaje.
- Estados: Operating, Alert, Critical, Completed y Failed.
- Damage Pad interactivo con amenazas móviles.
- Mini Damage Pad visible durante una misión.
- Estadísticas e historial.
- Simulación automática.
- Reportes finales.
- Backups JSON cargables.
- Menú de pausa con ESC.
- Abort Mission antes de alcanzar la victoria.
- Continuación indefinida después de la victoria.
- Sistema de audio dinámico según contexto.
- Control de volumen master.
- Efecto visual aleatorio de interferencia mediante buzz.gif.
- Interfaz adaptativa y centrada.


5. ALGORITMO PERSONALIZADO: DAMAGE PAD

El Damage Pad representa daños en un plano cartesiano. Cada daño aparece en
una posición aleatoria y se desplaza progresivamente hacia un terminal.

En cada actualización se calculan los movimientos que reducen la distancia
Manhattan entre el daño y el terminal. Si existen varias posibilidades, el
sistema utiliza random para seleccionar una de ellas.

Reparar un daño produce:

    Energy: -3
    Score:  +10

Después de una reparación, el daño desaparece y se generan dos nuevos daños.
Esto crea una decisión estratégica entre conservar energía o impedir que una
amenaza llegue al terminal.

Si un daño alcanza el terminal:

- se registra una brecha;
- se reproduce un efecto de daño;
- se elimina el daño;
- aparece un nuevo daño;
- se activa un evento de emergencia;
- el movimiento se pausa mientras el operador responde.

La velocidad depende de la dificultad.


6. SISTEMA DE AUDIO Y PRESENTACIÓN

El proyecto utiliza dos pistas musicales hechas con Logic Pro que funcionan simultáneamente con
mezcla dinámica:

- Mechanical Process.mp3: ambiente de menús y zonas fuera del gameplay.
- Mechanissues.mp3: música de la misión.

Durante el gameplay, la música de misión toma prioridad. Durante pausa, su
volumen se reduce. Los efectos de sonido utilizan canales separados.

El juego también incorpora un efecto visual de interferencia que aparece en
intervalos aleatorios para reforzar la estética de una terminal dañada.


7. REQUISITOS DEL RETO IMPLEMENTADOS

- Autenticación de usuario.
- Creación y carga de misiones.
- Gestión de recursos sin valores negativos.
- Eventos aleatorios.
- Decisiones y consecuencias.
- Uso funcional de random.
- Puntaje automático.
- Estados de misión.
- Historial.
- Estadísticas.
- Reporte final.
- Validación de datos.
- Persistencia JSON.
- Backups.
- Algoritmo propio documentado.


8. PERSISTENCIA

Las misiones se almacenan exclusivamente en:

    .data/missions.json

Si la carpeta .data no existe, el programa la crea automáticamente.

Los operadores se almacenan en:

    .data/operators.json

Los backups exportados se guardan en:

    Backups/


Diviértanse!

⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⡶⠿⠿⢛⣩⣭⣶⣶⣶⣶⣦⣭⣙⠿⣶⣤⣀⠀⠀⠀⠀
⠀⠀⠀⣾⠁⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠈⠛⠿⣷⡄⠀⠀
⠀⠀⢠⣿⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⣿⠀⠀
⠀⠀⢸⡟⣼⡿⢉⡉⢿⣿⡿⠿⠿⣿⣿⣿⠛⠛⣿⣧⠀⠀⣸⡿⠀⠀
⠀⠀⢸⡇⣿⡇⠘⠃⣸⠁⠀⠀⠀⠀⢹⡇⠸⠇⢸⣿⣷⠆⣿⡇⠀⠀
⠀⠀⠈⣿⡘⣿⢶⣶⡿⣦⣀⣀⣀⣠⣾⣷⣤⣤⢿⣿⣿⢰⡿⠁⠀⠀
⠀⠀⠀⠈⢷⣜⢿⣯⣿⣟⣡⣶⣌⠻⣿⣯⣿⣻⣿⡿⣡⣿⠁⠀⠀⠀
⠀⠀⠀⣀⣼⡇⢲⣈⣴⣶⡙⣿⡿⢋⣭⣉⣰⣶⣦⢰⣿⠁⠀⠀⠀⠀
⣠⡾⢟⣛⣋⣭⡤⢡⣿⣿⣧⣶⣦⡹⢛⣩⣴⣮⡉⢼⡏⠀⠀⠀⠀⠀
⢻⣦⡻⠿⢿⣿⢡⣿⠟⢋⣭⣭⠙⣰⣿⣿⠿⡋⢀⣾⣧⣤⣄⡀⠀⠀
⠀⠉⠻⠿⢷⡆⣿⡇⣾⢸⣿⡟⣴⣤⢠⣴⣶⣾⡌⠟⠋⠉⠙⠻⢷⣄
⠀⠀⠀⠀⢸⡇⢿⣿⣎⢘⣿⣇⠛⣫⣼⣿⣿⣿⠇⠀⠀⠀⠀⠀⣀⡿
⠀⠀⠀⠀⠘⢷⡘⢿⣿⣦⣬⣥⣵⣿⣿⣿⣿⠟⣀⣠⣤⣴⠶⠛⠉⠀
⠀⠀⠀⠀⢀⣼⠟⠂⠉⠛⠛⠿⠿⠿⠟⠛⠁⠘⢿⣿⡉⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⡃⠀⠀⠀⢀⣾⡿⠿⢿⣧⠀⠀⠀⠀⢹⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠛⠿⠿⠿⠿⠟⠉⠀⠀⠈⠛⠿⠿⠿⠿⠿⠋⠀⠀⠀⠀⠀