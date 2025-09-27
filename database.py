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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales (
                id TEXT PRIMARY KEY,
                especie TEXT NOT NULL,
                peso REAL NOT NULL,
                fecha_nac DATE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veterinarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos_sanitarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                fecha DATE NOT NULL,
                medicamento TEXT NOT NULL,
                veterinario_id INTEGER,
                FOREIGN KEY (animal_id) REFERENCES animales (id)
            )
        ''')
        
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
    
    # CRUD Animales
    def agregar_animal(self, animal):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO animales VALUES (?, ?, ?, ?)', 
                      (animal.id, animal.especie, animal.peso, animal.fecha_nac))
        conn.commit()
        conn.close()
    
    def obtener_animales(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animales ORDER BY id')
        animales = cursor.fetchall()
        conn.close()
        return animales
    
    # CRUD Veterinarios
    def agregar_veterinario(self, veterinario):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO veterinarios (nombre, especialidad) VALUES (?, ?)', 
                      (veterinario.nombre, veterinario.especialidad))
        conn.commit()
        conn.close()
    
    def obtener_veterinarios(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veterinarios ORDER BY nombre')
        veterinarios = cursor.fetchall()
        conn.close()
        return veterinarios
    
    # CRUD Eventos
    def registrar_evento(self, animal_id, evento):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO eventos_sanitarios (animal_id, tipo, fecha, medicamento) 
            VALUES (?, ?, ?, ?)
        ''', (animal_id, evento.tipo, evento.fecha, evento.medicamento))
        conn.commit()
        conn.close()
    
    # CRUD Producción
    def registrar_produccion(self, animal_id, produccion):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produccion (animal_id, tipo, cantidad, fecha) 
            VALUES (?, ?, ?, ?)
        ''', (animal_id, produccion.tipo, produccion.cantidad, produccion.fecha))
        conn.commit()
        conn.close()