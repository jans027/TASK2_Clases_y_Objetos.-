

from modelos.registro import Registro

class SistemaGanadero:
    def __init__(self):
        self.animales = []      # Lista de todos los animales del sistema
        self.veterinarios = []  # Lista de veterinarios registrados
        self.registros = []     # Historial de todos los registros
    
    def agregar_animal(self, animal):
        # Agrega un nuevo animal al sistema ganadero
        self.animales.append(animal)
    
    def agregar_veterinario(self, veterinario):
        # Agrega un veterinario al sistema
        self.veterinarios.append(veterinario)
    
    def registrar_evento(self, animal_id, evento):
        # Registra un evento sanitario para un animal
        animal = next((a for a in self.animales if a.id == animal_id), None)
        if animal:
            registro = Registro()
            registro.animal = animal
            registro.evento = evento
            self.registros.append(registro)
    
    def registrar_produccion(self, animal_id, produccion):
        # Registra datos de producción de un animal
        animal = next((a for a in self.animales if a.id == animal_id), None)
        if animal:
            registro = Registro()
            registro.animal = animal
            registro.produccion = produccion
            self.registros.append(registro)
    
    def consultar_datos(self):
        # Consulta y retorna datos del sistema
        return {
            'animales': len(self.animales),
            'veterinarios': len(self.veterinarios),
            'registros': len(self.registros)
        }