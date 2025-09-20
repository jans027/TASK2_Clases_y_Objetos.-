# TASK2_Clases_y_Objetos.-
# Sistema de Manejo Ganadero

Un programa de escritorio desarrollado en Python para la gestión básica de información ganadera, ideal para el aprendizaje de Programación Orientada a Objetos.


## Instrucciones 

**Para usuarios nuevos**: Ejecuta `main.py` y sigue las instrucciones en pantalla
Este README proporciona una guía completa para entender, instalar y utilizar el sistema de manejo ganadero.

## Características

- **Gestión de Animales**: Registro de datos básicos (ID, especie, peso, fecha nacimiento)
- **Eventos Sanitarios**: Control de vacunaciones y tratamientos médicos
- **Producción**: Seguimiento de producción de leche y carne
- **Veterinarios**: Administración de profesionales y sus actividades
- **Consultas**: Generación de reportes y búsquedas

## Estructura del Proyecto
sistema_ganadero/
│
├── modelos/
│ ├── init.py
│ ├── animal.py # Clase Animal
│ ├── evento_sanitario.py # Clase EventoSanitario
│ ├── produccion.py # Clase Produccion
│ ├── veterinario.py # Clase Veterinario
│ ├── registro.py # Clase Registro
│ ├── consulta.py # Clase Consulta
│ └── sistema_ganadero.py # Clase principal
│
└── main.py # Programa principal



## Instalación y Ejecución

1. **Requisitos**:
   - Python 3.6 o superior
   - No se requieren librerías externas

2. **Ejecución**:
   ```bash
   # Clona o descarga los archivos
   git clone <url-del-repositorio>
   
   # Navega al directorio
   cd sistema_ganadero
   
   # Ejecuta el programa
   python main.py


## Uso del Programa
Menú Principal:

====================================
   SISTEMA DE MANEJO GANADERO
====================================

--- MENÚ PRINCIPAL ---
1. Agregar animal
2. Agregar veterinario
3. Registrar evento sanitario
4. Registrar producción
5. Consultar datos
6. Salir

# Ejemplo de Flujo:

    Agregar Animal:

        ID: 001

        Especie: Vaca

        Peso: 450 kg

        Fecha nacimiento: 2020-05-15

    Registrar Evento:

        Tipo: Vacunación

        Medicamento: Piroxican

        Fecha: 2024-01-20

    Consultar Datos:

        Muestra estadísticas y listados

# Clases Implementadas
1. Animal

    Gestiona información básica de cada animal

    Calcula automáticamente la edad

2. EventoSanitario

    Registra tratamientos médicos

    Lleva control de medicamentos utilizados

3. Produccion

    Controla producción de leche y carne

    Registra cantidades y fechas

4. Veterinario

    Administra información de profesionales

    Relaciona veterinarios con eventos realizados

5. SistemaGanadero

    Clase principal que coordina todas las operaciones

    Gestiona las listas de animales, veterinarios y registros

# Propósito Educativo

Este proyecto está diseñado específicamente para:

    Aprender Programación Orientada a Objetos

    Entender relaciones entre clases (asociaciones, multiplicidades)

    Practicar implementación de UML en código

    Desarrollar habilidades en Python básico

# Tecnologías Utilizadas

    Lenguaje: Python 3

    Paradigma: Programación Orientada a Objetos (POO)

    Persistencia: Memoria (los datos se pierden al cerrar el programa)

    Interfaz: Consola/terminal

# Diagrama UML

El sistema sigue un diagrama de clases UML que incluye:

    Relaciones de asociación entre clases

    Multiplicidades (1, 0.., 1..)

    Atributos y métodos principales


# Licencia

Este proyecto es de código abierto y está disponible para fines educativos.