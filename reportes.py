import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from database import Database

class GeneradorReportesSimple:
    def __init__(self):
        self.db = Database()
    
    def generar_reporte_produccion_texto(self):
        """Genera reporte de producción en formato texto (sin gráficos)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Reporte básico de producción
        reporte = "=== REPORTE DE PRODUCCIÓN ===\n\n"
        
        # Total producción por tipo
        cursor.execute('''
            SELECT tipo, SUM(cantidad), COUNT(*) 
            FROM produccion 
            GROUP BY tipo
        ''')
        produccion_por_tipo = cursor.fetchall()
        
        reporte += "PRODUCCIÓN POR TIPO:\n"
        for tipo, total, conteo in produccion_por_tipo:
            reporte += f"- {tipo}: {total:.2f} unidades ({conteo} registros)\n"
        
        # Producción mensual
        cursor.execute('''
            SELECT strftime('%Y-%m', fecha) as mes, SUM(cantidad)
            FROM produccion 
            GROUP BY mes 
            ORDER BY mes
        ''')
        produccion_mensual = cursor.fetchall()
        
        reporte += "\nPRODUCCIÓN MENSUAL:\n"
        for mes, total in produccion_mensual:
            reporte += f"- {mes}: {total:.2f} unidades\n"
        
        # Top animales productivos
        cursor.execute('''
            SELECT a.id, a.especie, SUM(p.cantidad) as total
            FROM produccion p
            JOIN animales a ON p.animal_id = a.id
            GROUP BY a.id 
            ORDER BY total DESC 
            LIMIT 5
        ''')
        top_animales = cursor.fetchall()
        
        reporte += "\nTOP 5 ANIMALES MÁS PRODUCTIVOS:\n"
        for i, (id_animal, especie, total) in enumerate(top_animales, 1):
            reporte += f"{i}. {id_animal} ({especie}): {total:.2f} unidades\n"
        
        conn.close()
        return reporte
    
    def generar_reporte_sanitario_texto(self):
        """Genera reporte sanitario en formato texto"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        reporte = "=== REPORTE SANITARIO ===\n\n"
        
        # Eventos por tipo
        cursor.execute('''
            SELECT tipo, COUNT(*), GROUP_CONCAT(DISTINCT medicamento)
            FROM eventos_sanitarios 
            GROUP BY tipo
        ''')
        eventos_por_tipo = cursor.fetchall()
        
        reporte += "EVENTOS SANITARIOS POR TIPO:\n"
        for tipo, conteo, medicamentos in eventos_por_tipo:
            reporte += f"- {tipo}: {conteo} eventos (Medicamentos: {medicamentos})\n"
        
        # Veterinarios más activos
        cursor.execute('''
            SELECT v.nombre, COUNT(e.id) as total_eventos
            FROM eventos_sanitarios e
            JOIN veterinarios v ON e.veterinario_id = v.id
            GROUP BY v.id 
            ORDER BY total_eventos DESC
        ''')
        veterinarios_activos = cursor.fetchall()
        
        reporte += "\nVETERINARIOS MÁS ACTIVOS:\n"
        for nombre, total in veterinarios_activos:
            reporte += f"- {nombre}: {total} eventos\n"
        
        conn.close()
        return reporte

    def mostrar_reporte_en_ventana(self, titulo, contenido):
        """Muestra el reporte en una ventana de texto"""
        ventana = tk.Toplevel()
        ventana.title(titulo)
        ventana.geometry("600x400")
        
        frame = ttk.Frame(ventana)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(frame, wrap='word')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert('1.0', contenido)
        text_widget.config(state='disabled') 
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

# Modificación en la interfaz para usar reportes simples
class InterfazGanaderaSimple:
    def __init__(self, root):
        # ... (código anterior igual)
        self.reportes = GeneradorReportesSimple()
        
    def crear_pestana_informes_simple(self):
        """Versión simple de la pestaña de informes sin gráficos"""
        frame_informes = ttk.Frame(self.notebook)
        self.notebook.add(frame_informes, text="Informes")
        
        frame_controles = ttk.Frame(frame_informes)
        frame_controles.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_controles, text="Reporte Producción", 
                command=self.mostrar_reporte_produccion).pack(side='left', padx=5)
        
        ttk.Button(frame_controles, text="Reporte Sanitario", 
                command=self.mostrar_reporte_sanitario).pack(side='left', padx=5)
        
        ttk.Button(frame_controles, text="Estadísticas Generales", 
                command=self.mostrar_estadisticas_generales).pack(side='left', padx=5)
        
        # Área para mostrar reportes
        self.frame_reporte = ttk.Frame(frame_informes)
        self.frame_reporte.pack(fill='both', expand=True, padx=10, pady=10)
    
    def mostrar_reporte_produccion(self):
        contenido = self.reportes.generar_reporte_produccion_texto()
        self.reportes.mostrar_reporte_en_ventana("Reporte de Producción", contenido)
    
    def mostrar_reporte_sanitario(self):
        contenido = self.reportes.generar_reporte_sanitario_texto()
        self.reportes.mostrar_reporte_en_ventana("Reporte Sanitario", contenido)
    
    def mostrar_estadisticas_generales(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Estadísticas generales
        estadisticas = "=== ESTADÍSTICAS GENERALES ===\n\n"
        
        # Contar animales
        cursor.execute('SELECT COUNT(*) FROM animales')
        total_animales = cursor.fetchone()[0]
        estadisticas += f"Total de animales: {total_animales}\n"
        
        # Contar eventos
        cursor.execute('SELECT COUNT(*) FROM eventos_sanitarios')
        total_eventos = cursor.fetchone()[0]
        estadisticas += f"Total de eventos sanitarios: {total_eventos}\n"
        
        # Contar producción
        cursor.execute('SELECT COUNT(*) FROM produccion')
        total_produccion = cursor.fetchone()[0]
        estadisticas += f"Total de registros de producción: {total_produccion}\n"
        
        # Producción total
        cursor.execute('SELECT SUM(cantidad) FROM produccion')
        suma_produccion = cursor.fetchone()[0] or 0
        estadisticas += f"Producción total: {suma_produccion:.2f} unidades\n"
        
        conn.close()
        
        self.reportes.mostrar_reporte_en_ventana("Estadísticas Generales", estadisticas)