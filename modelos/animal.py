

from datetime import date

class Animal:
    def __init__(self):
        self.id = None           # Identificador único del animal
        self.especie = None      # Especie del animal (ej: bovino, porcino)
        self.peso = None         # Peso actual del animal en kg
        self.fecha_nac = None    # Fecha de nacimiento del animal

    def get_edad(self):
        # Calcula y retorna la edad del animal en años
        if not self.fecha_nac:
            return "Fecha de nacimiento no registrada"
        
        hoy = date.today()
        edad = hoy.year - self.fecha_nac.year
        
        # Ajustar si aún no ha pasado el cumpleaños este año
        if (hoy.month, hoy.day) < (self.fecha_nac.month, self.fecha_nac.day):
            edad -= 1
            
        return edad

    def actualizar_peso(self, nuevo_peso):
        # Actualiza el peso del animal con el nuevo valor
        self.peso = nuevo_peso
        print(f"Peso actualizado: {self.peso}kg")
