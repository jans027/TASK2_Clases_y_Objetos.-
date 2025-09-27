import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='ganadero.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla Animales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales (
                id TEXT PRIMARY KEY,
                especie TEXT NOT NULL,
                peso REAL NOT NULL,
                fecha_nac DATE NOT NULL
            )
        ''')
        
        # Tabla Veterinarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veterinarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL
            )
        ''')
        
        # Tabla Eventos Sanitarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos_sanitarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                fecha DATE NOT NULL,
                medicamento TEXT NOT NULL,
                veterinario_id INTEGER,
                FOREIGN KEY (animal_id) REFERENCES animales (id),
                FOREIGN KEY (veterinario_id) REFERENCES veterinarios (id)
            )
        ''')
        
        # Tabla Producción
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                fecha DATE NOT NULL,
                FOREIGN KEY (animal_id) REFERENCES animales (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Métodos CRUD para Animales
    def agregar_animal(self, animal):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO animales (id, especie, peso, fecha_nac)
            VALUES (?, ?, ?, ?)
        ''', (animal.id, animal.especie, animal.peso, animal.fecha_nac))
        conn.commit()
        conn.close()
    
    def obtener_animales(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animales')
        animales = cursor.fetchall()
        conn.close()
        return animales
    
    def actualizar_animal(self, animal_id, nuevo_peso):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE animales SET peso = ? WHERE id = ?
        ''', (nuevo_peso, animal_id))
        conn.commit()
        conn.close()
    
    def eliminar_animal(self, animal_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM animales WHERE id = ?', (animal_id,))
        conn.commit()
        conn.close()