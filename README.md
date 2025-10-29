SISTEMA DE MANEJO GANADERO
====================================

Una aplicación completa para gestión ganadera con interfaz gráfica, 
base de datos y sistema de chat de soporte en tiempo real.

CARACTERÍSTICAS PRINCIPALES
-------------------------------
Gestión completa de animales
Registro de eventos sanitarios  
Control de producción (leche, carne, etc.)
Administración de veterinarios
Reportes automáticos
Base de datos SQLite integrada
Chat de soporte en tiempo real
Servidor de chat incorporado

REQUISITOS DEL SISTEMA
-------------------------
- Python 3.6 o superior
- Tkinter (generalmente incluido con Python)

INSTALACIÓN Y EJECUCIÓN
---------------------------

1. EJECUCIÓN RÁPIDA:
   Ejecutar interfaz.py


INSTRUCCIONES DE USO
-----------------------

1. PRIMER USO:
   - Al ejecutar se crea automáticamente la base de datos
   - El servidor de chat se inicia automáticamente
   - No se requiere configuración adicional

4. CHAT DE SOPORTE:

   - "Chat de Soporte": Abre ventana de chat
   - Ingresar nickname
   - Escribir mensajes y presionar Enter
   - El sistema responde automáticamente
   - Funciona en tiempo real con el servidor

SISTEMA DE CHAT DE SOPORTE
-----------------------------

NUEVA FUNCIONALIDAD INTEGRADA

El sistema ahora incluye un chat de soporte en tiempo real que permite:

- Comunicación instantánea con soporte técnico
- Respuestas automáticas inteligentes
- Múltiples clientes simultáneos
- Conexión/desconexión automática


NOTAS IMPORTANTES
--------------------

- La base de datos se guarda automáticamente (ganadero.db)
- Los datos persisten entre ejecuciones
- No eliminar ganadero.db para no perder información
- Formato de fecha debe ser exacto: AAAA-MM-DD
- El ID del animal debe ser único
- El servidor de chat usa puerto 5000

# Licencia

Este proyecto es de código abierto y está disponible para fines educativos.