import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
import threading
import socket
import time
import pygame
from laberinto import ejecutar_juego_laberinto

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

class ServidorSoporte:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clientes = {}
        self.socket_servidor = None
        self.activo = False
    
    def iniciar_servidor(self):
        """Inicia el servidor de soporte en un hilo separado"""
        try:
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind((self.host, self.port))
            self.socket_servidor.listen(5)
            self.socket_servidor.settimeout(1)  # Timeout para poder verificar self.activo
            self.activo = True
            
            print(f"Servidor de soporte iniciado en {self.host}:{self.port}")
            
            # Hilo para aceptar conexiones
            threading.Thread(target=self.aceptar_conexiones, daemon=True).start()
            
            return True
            
        except Exception as e:
            print(f"Error al iniciar servidor: {e}")
            return False
    
    def aceptar_conexiones(self):
        """Acepta conexiones entrantes de clientes"""
        while self.activo:
            try:
                cliente_socket, direccion = self.socket_servidor.accept()
                print(f"Nuevo cliente conectado: {direccion}")
                
                # Recibir nickname del cliente
                cliente_socket.settimeout(1)
                nickname = cliente_socket.recv(1024).decode('utf-8')
                self.clientes[cliente_socket] = {
                    'nickname': nickname,
                    'direccion': direccion,
                    'conectado': True
                }
                
                # Enviar mensaje de bienvenida
                mensaje_bienvenida = f"Bienvenido {nickname}! Te has conectado al soporte del Sistema Ganadero."
                cliente_socket.send(mensaje_bienvenida.encode('utf-8'))
                
                # Hilo para manejar mensajes del cliente
                threading.Thread(
                    target=self.manejar_cliente, 
                    args=(cliente_socket,), 
                    daemon=True
                ).start()
                
            except socket.timeout:
                continue  # Timeout normal, continuar verificando self.activo
            except Exception as e:
                if self.activo:
                    print(f"Error aceptando conexión: {e}")
    
    def manejar_cliente(self, cliente_socket):
        """Maneja los mensajes de un cliente específico"""
        cliente_info = self.clientes[cliente_socket]
        nickname = cliente_info['nickname']
        
        while self.activo and cliente_info['conectado']:
            try:
                mensaje = cliente_socket.recv(1024).decode('utf-8')
                
                if not mensaje:
                    break
                
                if mensaje.lower() == 'salir':
                    break
                
                print(f"[{nickname}]: {mensaje}")
                
                # Respuesta automática del sistema
                respuesta = self.generar_respuesta(mensaje, nickname)
                cliente_socket.send(respuesta.encode('utf-8'))
                    
            except socket.timeout:
                continue
            except:
                break
        
        # Desconectar cliente
        self.desconectar_cliente(cliente_socket)
    
    def generar_respuesta(self, mensaje, nickname):
        """Genera respuesta automática basada en el mensaje"""
        mensaje_lower = mensaje.lower()
        
        if any(palabra in mensaje_lower for palabra in ['hola', 'buenas', 'saludos']):
            return f"Soporte: ¡Hola {nickname}! ¿En qué puedo ayudarte con el Sistema Ganadero?"
        elif any(palabra in mensaje_lower for palabra in ['error', 'problema', 'no funciona']):
            return "Soporte: Lamentamos los inconvenientes. Por favor describe el problema en detalle."
        elif any(palabra in mensaje_lower for palabra in ['gracias', 'agradezco']):
            return f"Soporte: ¡De nada {nickname}! ¿Necesitas ayuda con algo más?"
        elif any(palabra in mensaje_lower for palabra in ['animal', 'registrar', 'agregar']):
            return "Soporte: Para registrar animales, ve a 'Agregar Animal' en el menú principal."
        elif any(palabra in mensaje_lower for palabra in ['veterinario', 'doctor']):
            return "Soporte: Puedes agregar veterinarios en 'Agregar Veterinario'."
        elif any(palabra in mensaje_lower for palabra in ['producción', 'leche', 'carne']):
            return "Soporte: El registro de producción está en 'Registrar Producción'."
        else:
            return "Soporte: He recibido tu mensaje. Un agente te atenderá pronto."
    
    def desconectar_cliente(self, cliente_socket):
        """Desconecta un cliente y limpia recursos"""
        if cliente_socket in self.clientes:
            nickname = self.clientes[cliente_socket]['nickname']
            self.clientes[cliente_socket]['conectado'] = False
            
            try:
                cliente_socket.close()
            except:
                pass
            
            del self.clientes[cliente_socket]
            print(f"Cliente desconectado: {nickname}")
    
    def detener_servidor(self):
        """Detiene el servidor"""
        print("Deteniendo servidor...")
        self.activo = False
        
        for cliente_socket in list(self.clientes.keys()):
            self.desconectar_cliente(cliente_socket)
        
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass

class ClienteChat:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket_cliente = None
        self.nickname = ""
        self.conectado = False
        self.callback_mensaje = None
    
    def conectar(self, nickname, callback_mensaje=None):
        """Conecta al servidor de chat"""
        try:
            self.nickname = nickname
            self.callback_mensaje = callback_mensaje
            
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.settimeout(1)
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            
            # Enviar nickname
            self.socket_cliente.send(nickname.encode('utf-8'))
            
            # Hilo para recibir mensajes
            threading.Thread(target=self.recibir_mensajes, daemon=True).start()
            
            return True
            
        except Exception as e:
            print(f"Error conectando: {e}")
            return False
    
    def recibir_mensajes(self):
        """Recibe mensajes del servidor"""
        while self.conectado:
            try:
                mensaje = self.socket_cliente.recv(1024).decode('utf-8')
                if mensaje and self.callback_mensaje:
                    self.callback_mensaje(mensaje)
            except socket.timeout:
                continue
            except:
                break
        
        self.conectado = False
        if self.callback_mensaje:
            self.callback_mensaje("Desconectado del servidor")
    
    def enviar_mensaje(self, mensaje):
        """Envía mensaje al servidor"""
        if self.conectado and self.socket_cliente:
            try:
                self.socket_cliente.send(mensaje.encode('utf-8'))
                return True
            except:
                self.conectado = False
                return False
        return False
    
    def desconectar(self):
        """Desconecta del servidor"""
        self.conectado = False
        if self.socket_cliente:
            try:
                self.socket_cliente.send("salir".encode('utf-8'))
                self.socket_cliente.close()
            except:
                pass

class InterfazSimple:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Ganadero")
        self.root.geometry("500x500")
        
        # Iniciar servidor automáticamente
        self.servidor = ServidorSoporte()
        self.servidor.iniciar_servidor()
        
        # Cliente de chat
        self.cliente_chat = None
        
        self.db = Database()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema Ganadero", 
                        font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Estado del servidor
        estado_frame = ttk.Frame(main_frame)
        estado_frame.pack(pady=5)
        
        self.lbl_estado_servidor = ttk.Label(estado_frame, 
                                        text="Servidor activo", 
                                        foreground="green")
        self.lbl_estado_servidor.pack()
        
        # Botones principales
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=20)
        
        ttk.Button(botones_frame, text="Agregar Animal", 
                command=self.agregar_animal, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Agregar Veterinario", 
                command=self.agregar_veterinario, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Registrar Evento", 
                command=self.registrar_evento, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Registrar Producción", 
                command=self.registrar_produccion, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Ver Animales", 
                command=self.ver_animales, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Ver Reportes", 
                command=self.ver_reportes, width=20).pack(pady=5)
        
        ttk.Button(botones_frame, text="Chat de Soporte", 
                command=self.abrir_chat_soporte, width=20).pack(pady=5)
        
        # Información rápida
        info_frame = ttk.LabelFrame(main_frame, text="Resumen", padding="30")
        info_frame.pack(fill='x', pady=10)
        
        self.actualizar_resumen(info_frame)
        
        # Botón de salida
        ttk.Button(main_frame, text="Salir", 
                command=self.salir, width=20).pack(pady=80)
        # Botón de laberinto
        ttk.Button(botones_frame, text="Juego Relajante", 
                command=self.jugar_laberinto, width=20).pack(pady=5)
        
    def actualizar_resumen(self, frame):
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
    
    def salir(self):
        """Cierra la aplicación correctamente"""
        if self.cliente_chat:
            self.cliente_chat.desconectar()
        self.servidor.detener_servidor()
        self.root.quit()
        self.root.destroy()
    
    def agregar_animal(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Animal")
        ventana.geometry("300x320")
        
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
                self.actualizar_resumen_desde_principal()
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def actualizar_resumen_desde_principal(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and child.cget('text') == "Resumen":
                        self.actualizar_resumen(child)
                        return
    
    def agregar_veterinario(self):
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
                self.actualizar_resumen_desde_principal()
                
            except Exception as e:
                messagebox.showerror("Error", f"Datos incorrectos: {e}")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def registrar_evento(self):
        animales = self.obtener_animales()
        if not animales:
            messagebox.showwarning("Advertencia", "Primero agrega animales")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Evento")
        ventana.geometry("300x330")
        
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
                self.actualizar_resumen_desde_principal()
                
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
                self.actualizar_resumen_desde_principal()
                
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
        ventana.geometry("400x320")
        
        frame = ttk.Frame(ventana)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=('ID', 'Especie', 'Peso', 'Fecha Nac.'), show='headings', height=10)
        
        tree.heading('ID', text='ID')
        tree.heading('Especie', text='Especie')
        tree.heading('Peso', text='Peso (kg)')
        tree.heading('Fecha Nac.', text='Fecha Nac.')
        
        tree.column('ID', width=80)
        tree.column('Especie', width=100)
        tree.column('Peso', width=80)
        tree.column('Fecha Nac.', width=100)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
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
        ventana.geometry("400x320")
        
        text_area = tk.Text(ventana, wrap='word', width=50, height=15)
        scrollbar = ttk.Scrollbar(ventana, orient='vertical', command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        reporte = self.generar_reporte_simple()
        text_area.insert('1.0', reporte)
        text_area.config(state='disabled')
        
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def generar_reporte_simple(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        reporte = "=== REPORTE GANADERO ===\n\n"
        
        cursor.execute('SELECT COUNT(*) FROM animales')
        total_animales = cursor.fetchone()[0]
        reporte += f"Total animales: {total_animales}\n"
        
        cursor.execute('SELECT COUNT(*) FROM veterinarios')
        total_veterinarios = cursor.fetchone()[0]
        reporte += f"Total veterinarios: {total_veterinarios}\n"
        
        cursor.execute('SELECT COUNT(*) FROM eventos_sanitarios')
        total_eventos = cursor.fetchone()[0]
        reporte += f"Total eventos: {total_eventos}\n"
        
        cursor.execute('SELECT COUNT(*), SUM(cantidad) FROM produccion')
        total_prod, suma_prod = cursor.fetchone()
        reporte += f"Registros producción: {total_prod}\n"
        reporte += f"Producción total: {suma_prod or 0:.2f} unidades\n\n"
        
        cursor.execute('SELECT tipo, SUM(cantidad) FROM produccion GROUP BY tipo')
        prod_tipo = cursor.fetchall()
        if prod_tipo:
            reporte += "PRODUCCIÓN POR TIPO:\n"
            for tipo, total in prod_tipo:
                reporte += f"  {tipo}: {total:.2f}\n"
        
        cursor.execute('SELECT nombre, especialidad FROM veterinarios')
        veterinarios = cursor.fetchall()
        if veterinarios:
            reporte += "\nVETERINARIOS:\n"
            for nombre, especialidad in veterinarios:
                reporte += f"  {nombre} - {especialidad}\n"
        
        conn.close()
        return reporte
    
    def abrir_chat_soporte(self):
        """Abre la ventana de chat de soporte REAL"""
        ventana_chat = tk.Toplevel(self.root)
        ventana_chat.title("Chat de Soporte - Conectado")
        ventana_chat.geometry("500x400")
        ventana_chat.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_chat(ventana_chat))
        
        main_frame = ttk.Frame(ventana_chat, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Estado de conexión
        estado_frame = ttk.Frame(main_frame)
        estado_frame.pack(fill='x', pady=5)
        
        self.lbl_estado_chat = ttk.Label(estado_frame, text="Conectando...")
        self.lbl_estado_chat.pack()
        
        # Área de mensajes
        frame_mensajes = ttk.LabelFrame(main_frame, text="Chat en Tiempo Real", padding="5")
        frame_mensajes.pack(fill='both', expand=True, pady=10)
        
        self.text_mensajes = scrolledtext.ScrolledText(frame_mensajes, height=15, wrap='word', state='disabled')
        self.text_mensajes.pack(fill='both', expand=True)
        
        # Entrada de mensaje
        frame_entrada = ttk.Frame(main_frame)
        frame_entrada.pack(fill='x', pady=5)
        
        ttk.Label(frame_entrada, text="Nickname:").pack(side='left', padx=5)
        self.entry_nickname = ttk.Entry(frame_entrada, width=15)
        self.entry_nickname.pack(side='left', padx=5)
        self.entry_nickname.insert(0, "Usuario")
        
        ttk.Label(frame_entrada, text="Mensaje:").pack(side='left', padx=5)
        self.entry_mensaje = ttk.Entry(frame_entrada, width=30)
        self.entry_mensaje.pack(side='left', padx=5)
        self.entry_mensaje.bind('<Return>', lambda e: self.enviar_mensaje_chat())
        
        # Botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="Enviar Mensaje", 
                command=self.enviar_mensaje_chat).pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="Desconectar", 
                command=lambda: self.cerrar_chat(ventana_chat)).pack(side='left', padx=5)
        
        # Conectar al chat
        self.conectar_al_chat()
    
    def agregar_mensaje_chat(self, mensaje):
        """Agrega un mensaje al área de chat"""
        self.text_mensajes.config(state='normal')
        self.text_mensajes.insert('end', mensaje + '\n')
        self.text_mensajes.see('end')
        self.text_mensajes.config(state='disabled')
    
    def conectar_al_chat(self):
        """Conecta al servidor de chat"""
        nickname = self.entry_nickname.get().strip()
        if not nickname:
            nickname = "Usuario"
        
        self.cliente_chat = ClienteChat()
        if self.cliente_chat.conectar(nickname, self.agregar_mensaje_chat):
            self.lbl_estado_chat.config(text="Conectado al servidor", foreground="green")
            self.agregar_mensaje_chat(f"Sistema: Conectado como '{nickname}'")
        else:
            self.lbl_estado_chat.config(text="No se pudo conectar", foreground="red")
            self.agregar_mensaje_chat("Sistema: Error al conectar con el servidor")
    
    def enviar_mensaje_chat(self):
        """Envía un mensaje a través del chat"""
        if not self.cliente_chat or not self.cliente_chat.conectado:
            messagebox.showerror("Error", "No estás conectado al servidor")
            return
        
        mensaje = self.entry_mensaje.get().strip()
        if not mensaje:
            return
        
        # Mostrar mensaje localmente
        self.agregar_mensaje_chat(f"Tú: {mensaje}")
        self.entry_mensaje.delete(0, 'end')
        
        # Enviar al servidor
        if not self.cliente_chat.enviar_mensaje(mensaje):
            self.agregar_mensaje_chat("Sistema: Error al enviar mensaje")
    
    def cerrar_chat(self, ventana):
        """Cierra la ventana de chat"""
        if self.cliente_chat:
            self.cliente_chat.desconectar()
        ventana.destroy()

    def jugar_laberinto(self):
        "Se ejecuta el juego en ventana separada"
        def ejecutar_en_hilo():
            try:
                # Mostrar mensaje de información
                messagebox.showinfo(
                    "Juego de Laberinto", 
                    "Instrucciones:\n\n"
                    "• Flechas: Mover al jugador (azul)\n"
                    "• R: Reiniciar juego\n"
                    "• ESC: Salir del juego\n\n"
                    "Objetivo: Llevar al jugador desde la entrada (verde) "
                    "hasta la salida (roja) en el menor tiempo posible."
                )
                
                # Ejecutar el juego
                ejecutar_juego_laberinto()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo iniciar el juego: {e}")
        
        # Ejecutar en hilo separado para no bloquear la interfaz principal
        import threading
        threading.Thread(target=ejecutar_en_hilo, daemon=True).start()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = InterfazSimple(root)
        root.mainloop()
    except ImportError:
        print("Error: Tkinter no está instalado.")
        print("Instala con: sudo apt-get install python3-tk")