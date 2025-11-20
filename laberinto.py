import pygame
import random
import time
import sys

# Inicializar Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)

# Configuración del laberinto
ANCHO_CELDA = 30
FILAS = 15
COLUMNAS = 15
ANCHO_VENTANA = COLUMNAS * ANCHO_CELDA
ALTO_VENTANA = FILAS * ANCHO_CELDA + 50  # Espacio extra para el cronómetro

class Laberinto:
    def __init__(self):
        self.filas = FILAS
        self.columnas = COLUMNAS
        self.laberinto = []
        self.generar_laberinto()
        self.jugador_pos = [1, 1]  # Posición inicial
        self.salida_pos = [self.filas-2, self.columnas-2]  # Posición de salida
        self.tiempo_inicio = None
        self.tiempo_transcurrido = 0
        self.juego_terminado = False
        self.jugador_en_movimiento = False
    
    def generar_laberinto(self):
        # Inicializar laberinto lleno de paredes (1)
        self.laberinto = [[1 for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Usar algoritmo de profundidad para generar laberinto
        self._generar_recursivo(1, 1)
        
        # Asegurar entrada y salida
        self.laberinto[1][1] = 0  # Entrada
        self.laberinto[self.filas-2][self.columnas-2] = 0  # Salida
        
        # Asegurar que haya un camino
        self._asegurar_camino()
    
    def _generar_recursivo(self, x, y):
        self.laberinto[y][x] = 0  # Hacer celda camino
        
        # Direcciones: arriba, derecha, abajo, izquierda
        direcciones = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(direcciones)
        
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if (0 < nx < self.columnas-1 and 0 < ny < self.filas-1 and 
                self.laberinto[ny][nx] == 1):
                # Quitar pared entre celdas
                self.laberinto[y + dy//2][x + dx//2] = 0
                self._generar_recursivo(nx, ny)
    
    def _asegurar_camino(self):
        # BFS para asegurar que hay camino desde entrada a salida
        visitado = [[False for _ in range(self.columnas)] for _ in range(self.filas)]
        cola = [(1, 1)]  # Desde la entrada
        visitado[1][1] = True
        
        while cola:
            x, y = cola.pop(0)
            
            # Si llegamos a la salida, hay camino
            if (x, y) == (self.columnas-2, self.filas-2):
                return True
            
            # Verificar vecinos
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.columnas and 0 <= ny < self.filas and 
                    not visitado[ny][nx] and self.laberinto[ny][nx] == 0):
                    visitado[ny][nx] = True
                    cola.append((nx, ny))
        
        # Si no hay camino, crear uno
        self._crear_camino_manual()
        return False
    
    def _crear_camino_manual(self):
        # Crear un camino directo desde entrada a salida
        for i in range(1, self.filas-1):
            self.laberinto[i][1] = 0
        for j in range(1, self.columnas-1):
            self.laberinto[self.filas-2][j] = 0
    
    def mover_jugador(self, dx, dy):
        if self.juego_terminado:
            return False
        
        nueva_x = self.jugador_pos[0] + dx
        nueva_y = self.jugador_pos[1] + dy
        
        # Verificar límites y colisiones
        if (0 <= nueva_x < self.columnas and 0 <= nueva_y < self.filas and 
            self.laberinto[nueva_y][nueva_x] == 0):
            
            # Iniciar cronómetro en el primer movimiento
            if not self.jugador_en_movimiento:
                self.tiempo_inicio = time.time()
                self.jugador_en_movimiento = True
            
            self.jugador_pos = [nueva_x, nueva_y]
            
            # Verificar si llegó a la salida
            if nueva_x == self.salida_pos[0] and nueva_y == self.salida_pos[1]:
                self.juego_terminado = True
                self.tiempo_transcurrido = time.time() - self.tiempo_inicio
            
            return True
        return False
    
    def obtener_tiempo(self):
        if self.juego_terminado:
            return self.tiempo_transcurrido
        elif self.jugador_en_movimiento:
            return time.time() - self.tiempo_inicio
        else:
            return 0
    
    def reiniciar(self):
        self.jugador_pos = [1, 1]
        self.tiempo_inicio = None
        self.tiempo_transcurrido = 0
        self.juego_terminado = False
        self.jugador_en_movimiento = False

class JuegoLaberinto:
    def __init__(self):
        self.pantalla = None
        self.reloj = pygame.time.Clock()
        self.laberinto = Laberinto()
        self.fuente = pygame.font.Font(None, 36)
    
    def iniciar(self):
        if not self.pantalla:
            self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
            pygame.display.set_caption("Laberinto Relajante - Sistema Ganadero")
        
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    elif evento.key == pygame.K_r:
                        self.laberinto.reiniciar()
                    elif not self.laberinto.juego_terminado:
                        if evento.key == pygame.K_UP:
                            self.laberinto.mover_jugador(0, -1)
                        elif evento.key == pygame.K_DOWN:
                            self.laberinto.mover_jugador(0, 1)
                        elif evento.key == pygame.K_LEFT:
                            self.laberinto.mover_jugador(-1, 0)
                        elif evento.key == pygame.K_RIGHT:
                            self.laberinto.mover_jugador(1, 0)
            
            self.dibujar()
            self.reloj.tick(60)
        
        pygame.quit()
    
    def dibujar(self):
        self.pantalla.fill(BLANCO)
        
        # Dibujar laberinto
        for y in range(self.laberinto.filas):
            for x in range(self.laberinto.columnas):
                rect = pygame.Rect(x * ANCHO_CELDA, y * ANCHO_CELDA, ANCHO_CELDA, ANCHO_CELDA)
                
                if self.laberinto.laberinto[y][x] == 1:  # Pared
                    pygame.draw.rect(self.pantalla, NEGRO, rect)
                else:  # Camino
                    pygame.draw.rect(self.pantalla, BLANCO, rect)
                    pygame.draw.rect(self.pantalla, GRIS, rect, 1)
        
        # Dibujar entrada (verde)
        entrada_rect = pygame.Rect(1 * ANCHO_CELDA, 1 * ANCHO_CELDA, ANCHO_CELDA, ANCHO_CELDA)
        pygame.draw.rect(self.pantalla, VERDE, entrada_rect)
        
        # Dibujar salida (roja)
        salida_rect = pygame.Rect(
            self.laberinto.salida_pos[0] * ANCHO_CELDA, 
            self.laberinto.salida_pos[1] * ANCHO_CELDA, 
            ANCHO_CELDA, ANCHO_CELDA
        )
        pygame.draw.rect(self.pantalla, ROJO, salida_rect)
        
        # Dibujar jugador (azul)
        jugador_rect = pygame.Rect(
            self.laberinto.jugador_pos[0] * ANCHO_CELDA, 
            self.laberinto.jugador_pos[1] * ANCHO_CELDA, 
            ANCHO_CELDA, ANCHO_CELDA
        )
        pygame.draw.rect(self.pantalla, AZUL, jugador_rect)
        
        # Dibujar información
        tiempo = self.laberinto.obtener_tiempo()
        texto_tiempo = self.fuente.render(f"Tiempo: {tiempo:.2f}s", True, NEGRO)
        self.pantalla.blit(texto_tiempo, (10, ALTO_VENTANA - 40))
        
        if self.laberinto.juego_terminado:
            texto_felicitaciones = self.fuente.render("¡Felicidades! Ganaste.", True, VERDE)
            self.pantalla.blit(texto_felicitaciones, (ANCHO_VENTANA // 2 - 150, ALTO_VENTANA - 40))
        
        # Instrucciones
        texto_instrucciones = self.fuente.render("Flechas: Moverse | R: Reiniciar | ESC: Salir", True, NEGRO)
        self.pantalla.blit(texto_instrucciones, (ANCHO_VENTANA // 2 - 200, 10))
        
        pygame.display.flip()

# Función para integrar con el sistema ganadero
def ejecutar_juego_laberinto():
    """Ejecuta el juego del laberinto desde el sistema ganadero"""
    try:
        juego = JuegoLaberinto()
        juego.iniciar()
        return True
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
        return False