import socket
import threading
import time

class ClienteSoporte:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket_cliente = None
        self.nickname = ""
        self.conectado = False
    
    def conectar_servidor(self):
        """Intenta conectar con el servidor de soporte"""
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.settimeout(5)  # Timeout de 5 segundos
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            return True
            
        except socket.timeout:
            print("Timeout: El servidor no responde")
            return False
        except ConnectionRefusedError:
            print("Error: No se puede conectar al servidor")
            return False
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def enviar_nickname(self, nickname):
        """Envía el nickname al servidor"""
        try:
            self.nickname = nickname
            self.socket_cliente.send(nickname.encode('utf-8'))
            return True
        except:
            return False
    
    def recibir_mensajes(self):
        """Recibe mensajes del servidor en un hilo separado"""
        while self.conectado:
            try:
                mensaje = self.socket_cliente.recv(1024).decode('utf-8')
                if not mensaje:
                    break
                print(f"\n{mensaje}")
                print("Tú: ", end="", flush=True)  # Prompt para nuevo mensaje
            except:
                break
        
        if self.conectado:
            print("\nDesconectado del servidor")
            self.conectado = False
    
    def enviar_mensajes(self):
        """Envía mensajes al servidor"""
        while self.conectado:
            try:
                mensaje = input("Tú: ")
                
                if mensaje.lower() == 'salir':
                    self.desconectar()
                    break
                
                self.socket_cliente.send(mensaje.encode('utf-8'))
                
            except Exception as e:
                print(f"Error enviando mensaje: {e}")
                break
    
    def desconectar(self):
        """Desconecta del servidor"""
        self.conectado = False
        if self.socket_cliente:
            try:
                self.socket_cliente.close()
            except:
                pass
    
    def iniciar_chat(self):
        """Inicia la sesión de chat"""
        print(f"\nConectado como: {self.nickname}")
        print("Escribe 'salir' para desconectarte")
        print("-" * 40)
        
        # Hilo para recibir mensajes
        threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        
        # Hilo principal para enviar mensajes
        self.enviar_mensajes()

def probar_conexion():
    """Función para probar la conexión con el servidor"""
    print("Probando conexión con el servidor...")
    
    cliente = ClienteSoporte()
    if cliente.conectar_servidor():
        cliente.desconectar()
        return True
    else:
        return False

def main():
    """Función principal del cliente"""
    print("=" * 50)
    print("SISTEMA DE SOPORTE GANADERO - CLIENTE")
    print("=" * 50)
    
    # Solicitar nickname
    nickname = input("Ingresa tu NickName: ").strip()
    if not nickname:
        nickname = "Usuario"
    
    # Intentar conexión
    cliente = ClienteSoporte()
    
    print(f"\nConectando al servidor...")
    if cliente.conectar_servidor():
        if cliente.enviar_nickname(nickname):
            cliente.iniciar_chat()
        else:
            print("Error al enviar nickname")
    else:
        print("\nEl servicio de soporte no está disponible en este momento.")
        print("   Por favor, intenta más tarde o contacta al administrador.")

if __name__ == "__main__":
    main()