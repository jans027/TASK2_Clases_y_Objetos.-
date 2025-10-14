SISTEMA DE MANEJO GANADERO
===========================

Una aplicación simple para gestionar información ganadera desarrollada en Python.

CARACTERÍSTICAS PRINCIPALES
- Gestión de animales (registro y consulta)
- Control de eventos sanitarios
- Registro de producción (leche, carne, etc.)
- Administración de veterinarios
- Reportes automáticos
- Base de datos SQLite integrada

SCRIPT PRINCIPAL
-------------------
El archivo principal para ejecutar la aplicación es:
interfaz.py

REQUISITOS DEL SISTEMA
-------------------------
- Python 3.6 o superior
- Tkinter (generalmente incluido con Python)

INSTALACIÓN Y EJECUCIÓN
---------------------------

1. INSTALAR PYTHON (si no lo tienes):
   - Windows: Descargar desde python.org
   - Linux: sudo apt-get install python3 python3-tk
   - Mac: Usar Homebrew: brew install python-tk

2. EJECUTAR LA APLICACIÓN:
   Abre una terminal/consola y navega a la carpeta del proyecto, luego ejecuta:

   python interfaz.py

   O si tienes varias versiones de Python:
   python3 interfaz.py

3. SOLUCIÓN DE PROBLEMAS:
   Si aparece error con Tkinter:
   - En Ubuntu/Debian: sudo apt-get install python3-tk
   - En Windows: Reinstalar Python marcando "tcl/tk and IDLE"
   - En Mac: brew install python-tk

INSTRUCCIONES DE USO
-----------------------

1. PRIMER USO:
   - Al ejecutar la aplicación se crea automáticamente la base de datos
   - No se requiere configuración adicional

2. FLUJO DE TRABAJO RECOMENDADO:

   a) AGREGAR ANIMALES:
      - Click en "Agregar Animal"
      - Completar: ID, Especie, Peso, Fecha de nacimiento
      - Formato fecha: YYYY-MM-DD (ej: 2024-01-15)

   b) AGREGAR VETERINARIOS:
      - Click en "Agregar Veterinario" 
      - Ingresar nombre y especialidad

   c) REGISTRAR EVENTOS SANITARIOS:
      - Click en "Registrar Evento"
      - Seleccionar animal de la lista
      - Especificar tipo de evento y medicamento
      - Registrar fecha del evento

   d) REGISTRAR PRODUCCIÓN:
      - Click en "Registrar Producción"
      - Seleccionar animal
      - Especificar tipo y cantidad de producción
      - Registrar fecha

3. CONSULTAS Y REPORTES:

   - "Ver Animales": Muestra lista completa de animales registrados
   - "Ver Reportes": Genera reporte con estadísticas y resúmenes

4. DATOS DE EJEMPLO PARA PROBAR:

   Animal:
     ID: VACA001
     Especie: Vaca
     Peso: 450
     Fecha: 2020-05-15

   Evento:
     Tipo: Vacunación
     Medicamento: Piroxican
     Fecha: 2024-01-20

   Producción:
     Tipo: Leche
     Cantidad: 25.5
     Fecha: 2024-01-21


# Licencia

Este proyecto es de código abierto y está disponible para fines educativos.