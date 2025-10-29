import socket
import threading
import time
from datetime import datetime

class ServidorSoporte:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clientes = {}
        self.socket_servidor = None
        self.activo = False
    
    def iniciar_servidor(self):
        """Inicia el servidor de soporte"""
        try:
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind((self.host, self.port))
            self.socket_servidor.listen(5)
            self.activo = True
            
            print(f" Servidor de soporte iniciado en {self.host}:{self.port}")
            print(" Esperando conexiones de clientes...")
            
            # Hilo para aceptar conexiones
            threading.Thread(target=self.aceptar_conexiones, daemon=True).start()
            
            # Hilo para comandos del servidor
            threading.Thread(target=self.control_servidor, daemon=True).start()
            
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
                nickname = cliente_socket.recv(1024).decode('utf-8')
                self.clientes[cliente_socket] = {
                    'nickname': nickname,
                    'direccion': direccion,
                    'conectado': True
                }
                
                # Enviar mensaje de bienvenida
                mensaje_bienvenida = f"Bienvenido {nickname}! Te has conectado al soporte del Sistema Ganadero. Escribe 'salir' para desconectarte."
                cliente_socket.send(mensaje_bienvenida.encode('utf-8'))
                
                # Notificar a otros clientes
                self.broadcast(f"{nickname} se ha unido al chat de soporte", cliente_socket)
                
                # Hilo para manejar mensajes del cliente
                threading.Thread(
                    target=self.manejar_cliente, 
                    args=(cliente_socket,), 
                    daemon=True
                ).start()
                
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
                
                if not mensaje or mensaje.lower() == 'salir':
                    break
                
                print(f"[{nickname}]: {mensaje}")
                
                # Reenviar mensaje a todos los clientes (incluyendo al remitente)
                timestamp = datetime.now().strftime("%H:%M:%S")
                mensaje_formateado = f"[{timestamp}] {nickname}: {mensaje}"
                self.broadcast(mensaje_formateado)
                
                # Respuesta automática del sistema
                if "hola" in mensaje.lower() or "buenos" in mensaje.lower():
                    respuesta = f"[Sistema] Hola {nickname}! ¿En qué puedo ayudarte con el Sistema Ganadero?"
                    cliente_socket.send(respuesta.encode('utf-8'))
                elif "error" in mensaje.lower():
                    respuesta = "[Sistema] Lamentamos los errores. Por favor describe el problema en detalle."
                    cliente_socket.send(respuesta.encode('utf-8'))
                elif "gracias" in mensaje.lower():
                    respuesta = f"[Sistema] De nada {nickname}! ¿Necesitas ayuda con algo más?"
                    cliente_socket.send(respuesta.encode('utf-8'))
                    
            except Exception as e:
                print(f"Error con cliente {nickname}: {e}")
                break
        
        # Desconectar cliente
        self.desconectar_cliente(cliente_socket)
    
    def broadcast(self, mensaje, cliente_excluido=None):
        """Envía un mensaje a todos los clientes conectados"""
        clientes_a_eliminar = []
        
        for cliente_socket, info in self.clientes.items():
            if cliente_socket != cliente_excluido and info['conectado']:
                try:
                    cliente_socket.send(mensaje.encode('utf-8'))
                except:
                    clientes_a_eliminar.append(cliente_socket)
        
        # Eliminar clientes desconectados
        for cliente in clientes_a_eliminar:
            self.desconectar_cliente(cliente)
    
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
            
            # Notificar a otros clientes
            self.broadcast(f"{nickname} ha abandonado el chat")
    
    def control_servidor(self):
        """Permite controlar el servidor desde la consola"""
        while self.activo:
            try:
                comando = input("").lower()
                if comando == 'salir':
                    self.detener_servidor()
                    break
                elif comando == 'clientes':
                    print(f"Clientes conectados: {len(self.clientes)}")
                    for info in self.clientes.values():
                        print(f"  - {info['nickname']} ({info['direccion']})")
                elif comando == 'help':
                    print("Comandos disponibles: salir, clientes, help")
            except:
                pass
    
    def detener_servidor(self):
        """Detiene el servidor y desconecta todos los clientes"""
        print("Deteniendo servidor...")
        self.activo = False
        
        # Desconectar todos los clientes
        for cliente_socket in list(self.clientes.keys()):
            self.desconectar_cliente(cliente_socket)
        
        # Cerrar socket del servidor
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass
        
        print("Servidor detenido correctamente")

def main():
    """Función principal del servidor"""
    print("=" * 50)
    print("SISTEMA DE SOPORTE GANADERO - SERVIDOR")
    print("=" * 50)
    
    servidor = ServidorSoporte()
    
    if servidor.iniciar_servidor():
        print("\nComandos del servidor:")
        print("   'clientes' - Ver clientes conectados")
        print("   'salir' - Detener servidor")
        print("   'help' - Mostrar ayuda")
        print("\nServidor en ejecución...")
        
        # Mantener el programa principal activo
        try:
            while servidor.activo:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupción recibida...")
            servidor.detener_servidor()
    else:
        print("No se pudo iniciar el servidor")

if __name__ == "__main__":
    main()