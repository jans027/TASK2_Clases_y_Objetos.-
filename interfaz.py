import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

class InterfazSimple:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Ganadero Simple")
        self.root.geometry("400x450") 
        
        self.db = Database()
        
        # Crear interfaz minimalista
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema Ganadero", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Botones principales 
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=20)
        
        ttk.Button(botones_frame, text="Agregar Animal", 
                  command=self.agregar_animal, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Agregar Veterinario", 
                  command=self.agregar_veterinario, width=20).pack(pady=5)  # ¡NUEVO BOTÓN!
        
        ttk.Button(botones_frame, text="Registrar Evento", 
                  command=self.registrar_evento, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Registrar Producción", 
                  command=self.registrar_produccion, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Ver Animales", 
                  command=self.ver_animales, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Ver Reportes", 
                  command=self.ver_reportes, width=20).pack(pady=5)
        
        # Información rápida
        info_frame = ttk.LabelFrame(main_frame, text="Resumen", padding="10")
        info_frame.pack(fill='x', pady=10)
        
        self.actualizar_resumen(info_frame)
    
    def actualizar_resumen(self, frame):
        # Limpiar frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM animales')
        total_animales = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM eventos_sanitarios')
        total_eventos = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM produccion')
        total_produccion = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM veterinarios')
        total_veterinarios = cursor.fetchone()[0]
        
        conn.close()
        
        info_text = f"Animales: {total_animales} | Veterinarios: {total_veterinarios} | Eventos: {total_eventos} | Producción: {total_produccion}"
        ttk.Label(frame, text=info_text, font=('Arial', 10)).pack()
    
    def agregar_animal(self):
        # Ventana para agregar animal
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Animal")
        ventana.geometry("300x300")
        
        ttk.Label(ventana, text="ID del animal:").pack(pady=5)
        entry_id = ttk.Entry(ventana, width=20)
        entry_id.pack(pady=5)
        
        ttk.Label(ventana, text="Especie:").pack(pady=5)
        entry_especie = ttk.Entry(ventana, width=20)
        entry_especie.pack(pady=5)
        
        ttk.Label(ventana, text="Peso (kg):").pack(pady=5)
        entry_peso = ttk.Entry(ventana, width=20)
        entry_peso.pack(pady=5)
        
        ttk.Label(ventana, text="Fecha Nac. (YYYY-MM-DD):").pack(pady=5)
        entry_fecha = ttk.Entry(ventana, width=20)
        entry_fecha.pack(pady=5)
        
        def guardar():
            try:
                id = entry_id.get().strip()
                especie = entry_especie.get().strip()
                peso = float(entry_peso.get())
                fecha = entry_fecha.get().strip()
                
                datetime.strptime(fecha, '%Y-%m-%d')
                
                if not id or not especie:
                    raise ValueError("Completa todos los campos")
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO animales VALUES (?, ?, ?, ?)', 
                              (id, especie, peso, fecha))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Animal agregado")
                ventana.destroy()
                # Actualizar el resumen
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                self.actualizar_resumen(child)
                                break
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def agregar_veterinario(self):  # ¡NUEVO MÉTODO!
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Veterinario")
        ventana.geometry("300x200")
        
        ttk.Label(ventana, text="Nombre del veterinario:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=20)
        entry_nombre.pack(pady=5)
        
        ttk.Label(ventana, text="Especialidad:").pack(pady=5)
        entry_especialidad = ttk.Entry(ventana, width=20)
        entry_especialidad.pack(pady=5)
        
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                especialidad = entry_especialidad.get().strip()
                
                if not nombre or not especialidad:
                    raise ValueError("Completa todos los campos")
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO veterinarios (nombre, especialidad) VALUES (?, ?)', 
                              (nombre, especialidad))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Veterinario agregado")
                ventana.destroy()
                # Actualizar el resumen
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                self.actualizar_resumen(child)
                                break
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def registrar_evento(self):
        # Verificar que hay animales
        animales = self.obtener_animales()
        if not animales:
            messagebox.showwarning("Advertencia", "Primero agrega animales")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Evento")
        ventana.geometry("300x320")
        
        ttk.Label(ventana, text="Seleccionar animal:").pack(pady=5)
        combo_animal = ttk.Combobox(ventana, values=animales, state="readonly")
        combo_animal.pack(pady=5)
        
        ttk.Label(ventana, text="Tipo de evento:").pack(pady=5)
        combo_tipo = ttk.Combobox(ventana, values=["Vacunación", "Desparasitación", "Consulta", "Tratamiento"])
        combo_tipo.pack(pady=5)
        
        ttk.Label(ventana, text="Medicamento:").pack(pady=5)
        entry_medicamento = ttk.Entry(ventana, width=20)
        entry_medicamento.pack(pady=5)
        
        ttk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        entry_fecha = ttk.Entry(ventana, width=20)
        entry_fecha.pack(pady=5)
        
        def guardar():
            try:
                animal_seleccionado = combo_animal.get()
                if not animal_seleccionado:
                    raise ValueError("Selecciona un animal")
                
                animal_id = animal_seleccionado.split(" - ")[0]
                tipo = combo_tipo.get()
                medicamento = entry_medicamento.get()
                fecha = entry_fecha.get()
                
                datetime.strptime(fecha, '%Y-%m-%d')
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO eventos_sanitarios (animal_id, tipo, fecha, medicamento) 
                    VALUES (?, ?, ?, ?)
                ''', (animal_id, tipo, fecha, medicamento))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Evento registrado")
                ventana.destroy()
                # Actualizar el resumen
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                self.actualizar_resumen(child)
                                break
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def registrar_produccion(self):
        animales = self.obtener_animales()
        if not animales:
            messagebox.showwarning("Advertencia", "Primero agrega animales")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Producción")
        ventana.geometry("300x320")
        
        ttk.Label(ventana, text="Seleccionar animal:").pack(pady=5)
        combo_animal = ttk.Combobox(ventana, values=animales, state="readonly")
        combo_animal.pack(pady=5)
        
        ttk.Label(ventana, text="Tipo:").pack(pady=5)
        combo_tipo = ttk.Combobox(ventana, values=["Leche", "Carne", "Huevos", "Lana"])
        combo_tipo.pack(pady=5)
        
        ttk.Label(ventana, text="Cantidad:").pack(pady=5)
        entry_cantidad = ttk.Entry(ventana, width=20)
        entry_cantidad.pack(pady=5)
        
        ttk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        entry_fecha = ttk.Entry(ventana, width=20)
        entry_fecha.pack(pady=5)
        
        def guardar():
            try:
                animal_seleccionado = combo_animal.get()
                if not animal_seleccionado:
                    raise ValueError("Selecciona un animal")
                
                animal_id = animal_seleccionado.split(" - ")[0]
                tipo = combo_tipo.get()
                cantidad = float(entry_cantidad.get())
                fecha = entry_fecha.get()
                
                datetime.strptime(fecha, '%Y-%m-%d')
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO produccion (animal_id, tipo, cantidad, fecha) 
                    VALUES (?, ?, ?, ?)
                ''', (animal_id, tipo, cantidad, fecha))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Producción registrada")
                ventana.destroy()
                # Actualizar el resumen
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                self.actualizar_resumen(child)
                                break
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def obtener_animales(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, especie FROM animales ORDER BY id')
        animales = [f"{a[0]} - {a[1]}" for a in cursor.fetchall()]
        conn.close()
        return animales
    
    def ver_animales(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Animales")
        ventana.geometry("400x300")
        
        # Frame con scrollbar
        frame = ttk.Frame(ventana)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview simple
        tree = ttk.Treeview(frame, columns=('ID', 'Especie', 'Peso', 'Fecha Nac.'), show='headings', height=10)
        
        tree.heading('ID', text='ID')
        tree.heading('Especie', text='Especie')
        tree.heading('Peso', text='Peso (kg)')
        tree.heading('Fecha Nac.', text='Fecha Nac.')
        
        tree.column('ID', width=80)
        tree.column('Especie', width=100)
        tree.column('Peso', width=80)
        tree.column('Fecha Nac.', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Cargar datos
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animales ORDER BY id')
        for animal in cursor.fetchall():
            tree.insert('', 'end', values=animal)
        conn.close()
        
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def ver_reportes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Reportes")
        ventana.geometry("400x300")
        
        # Área de texto con scroll
        text_area = tk.Text(ventana, wrap='word', width=50, height=15)
        scrollbar = ttk.Scrollbar(ventana, orient='vertical', command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Generar reporte simple
        reporte = self.generar_reporte_simple()
        text_area.insert('1.0', reporte)
        text_area.config(state='disabled')  # Solo lectura
        
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def generar_reporte_simple(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        reporte = "=== REPORTE GANADERO ===\n\n"
        
        # Animales
        cursor.execute('SELECT COUNT(*) FROM animales')
        total_animales = cursor.fetchone()[0]
        reporte += f"Total animales: {total_animales}\n"
        
        # Veterinarios
        cursor.execute('SELECT COUNT(*) FROM veterinarios')
        total_veterinarios = cursor.fetchone()[0]
        reporte += f"Total veterinarios: {total_veterinarios}\n"
        
        # Eventos
        cursor.execute('SELECT COUNT(*) FROM eventos_sanitarios')
        total_eventos = cursor.fetchone()[0]
        reporte += f"Total eventos: {total_eventos}\n"
        
        # Producción
        cursor.execute('SELECT COUNT(*), SUM(cantidad) FROM produccion')
        total_prod, suma_prod = cursor.fetchone()
        reporte += f"Registros producción: {total_prod}\n"
        reporte += f"Producción total: {suma_prod or 0:.2f} unidades\n\n"
        
        # Producción por tipo
        cursor.execute('SELECT tipo, SUM(cantidad) FROM produccion GROUP BY tipo')
        prod_tipo = cursor.fetchall()
        if prod_tipo:
            reporte += "PRODUCCIÓN POR TIPO:\n"
            for tipo, total in prod_tipo:
                reporte += f"  {tipo}: {total:.2f}\n"
        
        # Veterinarios registrados
        cursor.execute('SELECT nombre, especialidad FROM veterinarios')
        veterinarios = cursor.fetchall()
        if veterinarios:
            reporte += "\nVETERINARIOS:\n"
            for nombre, especialidad in veterinarios:
                reporte += f"  {nombre} - {especialidad}\n"
        
        conn.close()
        return reporte

# Ejecutar la aplicación
if __name__ == "__main__":
    # Verificar si tkinter está disponible
    try:
        root = tk.Tk()
        app = InterfazSimple(root)
        root.mainloop()
    except ImportError:
        print("Error: Tkinter no está instalado.")
        print("Instala con: sudo apt-get install python3-tk")
        print("O ejecuta la versión de consola.")