# Sistema de Manejo Ganadero - Programa Principal
# Programa básico para aprendizaje de POO

from modelos.animal import Animal
from modelos.eventoSanitario import EventoSanitario
from modelos.produccion import Produccion
from modelos.veterinario import Veterinario
from modelos.sistemaGanadero import SistemaGanadero
from datetime import date

def main():
    print("====================================")
    print("   SISTEMA DE MANEJO GANADERO")
    print("====================================")
    
    # Crear sistema principal
    sistema = SistemaGanadero()
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Agregar animal")
        print("2. Agregar veterinario")
        print("3. Registrar evento sanitario")
        print("4. Registrar producción")
        print("5. Consultar datos")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_animal(sistema)
        elif opcion == "2":
            agregar_veterinario(sistema)
        elif opcion == "3":
            registrar_evento(sistema)
        elif opcion == "4":
            registrar_produccion(sistema)
        elif opcion == "5":
            consultar_datos(sistema)
        elif opcion == "6":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def agregar_animal(sistema):
    print("\n--- AGREGAR ANIMAL ---")
    id = input("ID del animal: ")
    especie = input("Especie: ")
    peso = float(input("Peso (kg): "))
    
    # Opción más simple: pedir fecha en formato texto y convertir
    fecha_str = input("Fecha de nacimiento (aaaa-mm-dd): ")
    
    try:
        # Convertir string a fecha
        anio, mes, dia = map(int, fecha_str.split('-'))
        fecha_nac = date(anio, mes, dia)
        
        animal = Animal()
        animal.id = id
        animal.especie = especie
        animal.peso = peso
        animal.fecha_nac = fecha_nac
        
        sistema.agregar_animal(animal)
        print("¡Animal agregado correctamente!")
        
    except ValueError:
        print("Formato de fecha incorrecto. Use aaaa-mm-dd")

def agregar_veterinario(sistema):
    print("\n--- AGREGAR VETERINARIO ---")
    nombre = input("Nombre: ")
    especialidad = input("Especialidad: ")
    
    vet = Veterinario()
    vet.nombre = nombre
    vet.especialidad = especialidad
    vet.eventos = []
    
    sistema.agregar_veterinario(vet)
    print("¡Veterinario agregado correctamente!")

def registrar_evento(sistema):
    print("\n--- REGISTRAR EVENTO SANITARIO ---")
    
    if not sistema.animales:
        print("No hay animales registrados.")
        return
    
    # Mostrar animales
    print("Animales disponibles:")
    for i, animal in enumerate(sistema.animales):
        print(f"{i+1}. {animal.id} - {animal.especie}")
    
    try:
        idx = int(input("Seleccione el número del animal: ")) - 1
        animal = sistema.animales[idx]
        
        tipo = input("Tipo de evento: ")
        medicamento = input("Medicamento utilizado: ")
        
        # Fecha del evento - FORMA CORREGIDA
        fecha_str = input("Fecha del evento (aaaa-mm-dd): ")
        
        try:
            # Dividir la fecha en partes
            anio, mes, dia = map(int, fecha_str.split('-'))
            fecha_evento = date(anio, mes, dia)
            
            evento = EventoSanitario()
            evento.tipo = tipo
            evento.fecha = fecha_evento
            evento.medicamento = medicamento
            
            sistema.registrar_evento(animal.id, evento)
            print("¡Evento registrado correctamente!")
            
        except ValueError:
            print("Formato de fecha incorrecto. Use aaaa-mm-dd")
        
    except (ValueError, IndexError):
        print("Selección no válida.")

def registrar_produccion(sistema):
    print("\n--- REGISTRAR PRODUCCIÓN ---")
    
    if not sistema.animales:
        print("No hay animales registrados.")
        return
    
    # Mostrar animales
    print("Animales disponibles:")
    for i, animal in enumerate(sistema.animales):
        print(f"{i+1}. {animal.id} - {animal.especie}")
    
    try:
        idx = int(input("Seleccione el número del animal: ")) - 1
        animal = sistema.animales[idx]
        
        tipo = input("Tipo de producción (leche/carne): ")
        cantidad = float(input("Cantidad: "))
        
        # Fecha de producción - FORMA CORREGIDA
        fecha_str = input("Fecha de producción (aaaa-mm-dd): ")
        
        try:
            anio, mes, dia = map(int, fecha_str.split('-'))
            fecha_prod = date(anio, mes, dia)
            
            produccion = Produccion()
            produccion.tipo = tipo
            produccion.cantidad = cantidad
            produccion.fecha = fecha_prod
            
            sistema.registrar_produccion(animal.id, produccion)
            print("¡Producción registrada correctamente!")
            
        except ValueError:
            print("Formato de fecha incorrecto. Use aaaa-mm-dd")
        
    except (ValueError, IndexError):
        print("Selección no válida.")

def consultar_datos(sistema):
    print("\n--- CONSULTAR DATOS ---")
    
    if not sistema.animales:
        print("No hay datos registrados.")
        return
    
    print(f"Total de animales: {len(sistema.animales)}")
    print(f"Total de veterinarios: {len(sistema.veterinarios)}")
    print(f"Total de registros: {len(sistema.registros)}")
    
    print("\nAnimales registrados:")
    for animal in sistema.animales:
        edad = animal.get_edad() if animal.fecha_nac else "N/A"
        print(f"- {animal.id} ({animal.especie}), {animal.peso}kg, Edad: {edad}")

if __name__ == "__main__":
    main()