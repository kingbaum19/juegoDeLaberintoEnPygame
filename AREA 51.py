#~~~~~~~~~~~~~~~~~~~~LIBRERÍAS Y MODULOS~~~~~~~~~~~~~~~~~~
import pygame
import random
import os
import csv
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

#~~~~~~~~~~~~~~~~~~~~TAMAÑO DE LAS CASILLAS Y VENTANA~~~~~~~~~~~~~~~~~~
pygame.init()
TILE_SIZE = 32
ALTO, ANCHO = 512, 512
WIN = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Escape de Area 51")
ICON = pygame.image.load(os.path.join('ASSETS','game_icon.png'))
pygame.display.set_icon(ICON)

MENSAJE = pygame.font.Font(os.path.join('FUENTES','NiseJSRF.TTF'),27)
FPS = 6

#~~~~~~~~~~~~~~~~~~~~SUPERFICIES~~~~~~~~~~~~~~~~~~

VOID = pygame.image.load(os.path.join('ASSETS','VOID.png'))
PORTAL = pygame.image.load(os.path.join('ASSETS','PORTAL.png'))
SUELO = pygame.image.load(os.path.join('ASSETS','SUELO.png'))
SPAWN = pygame.image.load(os.path.join('ASSETS','SPAWN.png'))
COIN = pygame.image.load(os.path.join('ASSETS','GHERKIN_ZONE.png'))
CASILLAS = [SUELO,VOID,PORTAL,SPAWN,COIN]

FILAS = 16
COLUMNAS = 16

ALIEN = pygame.image.load(os.path.join('ASSETS','ALIEN.png')).convert_alpha()
alien = ALIEN.get_rect()

#~~~~~~~~~~~~~~~~~~~~EFECTOS DE SONIDO~~~~~~~~~~~~~~~~~~~~~~~~~~
YAHOO_1 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO1.mp3'))
YAHOO_2 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO2.mp3'))
YAHOO_3 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO3.mp3'))
YAHOO_4 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO4.mp3'))
YAHOO_5 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO5.mp3'))
YAHOO_6 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO6.mp3'))
PORTAL_SOUNDS = [YAHOO_1,YAHOO_2,YAHOO_3,YAHOO_4,YAHOO_5,YAHOO_6]

PASOS = pygame.mixer.Sound(os.path.join('SONIDO', 'STEPS.WAV'))

canciones = os.listdir("OST")
cancion_actual = 0

#~~~~~~~~~~~~~~~~~~~~~~~~EVENTOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ALIEN_PORTAL = pygame.USEREVENT +1

#~~~~~~~~~~~~~~~~~~~~GENERACIÓN DE LABERINTO~~~~~~~~~~~~~~~~~~
def cargar_nivel(nivel):
    maze = []

    for fila in range(FILAS):
        filas = [0] * COLUMNAS
        maze.append(filas)

    with open(nivel, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, fila in enumerate(reader):
            for j, columna in enumerate(fila):
                maze[i][j] = int(columna)

    for fila in range(len(maze)): #Casilla en donde aparecerá el jugador
        for columna in range(len(maze[fila])):
            if maze[fila][columna] == 3:
                alien.x = columna * TILE_SIZE
                alien.y = fila * TILE_SIZE
    return maze

csv_files = os.listdir("NIVELES")
nivel_actual = 0
maze = cargar_nivel(os.path.join("NIVELES", csv_files[nivel_actual]))


#~~~~~~~~~~~~~~~~~~~~FUNCIONES DEL JUEGO~~~~~~~~~~~~~~~~~~
def draw_mensaje(texto):
    draw_text = MENSAJE.render(texto,1,(51,238,34))
    WIN.blit(draw_text,(ANCHO/2 - draw_text.get_width()/
                        2, ALTO/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_grid():
    for line in range(0,16):
        pygame.draw.line(WIN,(255,255,255),(0,line * TILE_SIZE),(ANCHO, line * TILE_SIZE))
        pygame.draw.line(WIN,(255,255,255),(line * TILE_SIZE, 0), (line * TILE_SIZE, ALTO))

def alien_movement(keys_pressed, alien):
    fila = int(alien.y / TILE_SIZE) 
    columna = int(alien.x/ TILE_SIZE)
    if keys_pressed[pygame.K_w]: #movimiento hacia arriba
        fila-=1
    elif keys_pressed[pygame.K_s]: #movimiento hacia abajo
        fila+=1
    elif keys_pressed[pygame.K_a]: #movimiento izquierdo
        columna-=1
    elif keys_pressed[pygame.K_d]: #movimiento derecho
        columna+=1
    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]:
        PASOS.play()
    casilla = CASILLAS[maze[fila][columna]]
    if casilla in [SUELO,PORTAL]:
        alien.x = columna * TILE_SIZE
        alien.y = fila * TILE_SIZE
    if casilla == PORTAL:
        pygame.event.post(pygame.event.Event(ALIEN_PORTAL))
        print ("Ha ganado")


def draw_window(alien):
    for fila in range(len(maze)):
        for columna in range (len(maze[fila])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE
            casilla = CASILLAS[maze[fila][columna]]
            WIN.blit(casilla,(x,y))

    WIN.blit(ALIEN,(alien.x, alien.y))
    pygame.display.update()


def main ():
    global nivel_actual, maze, cancion_actual
    pygame.mixer.music.load(os.path.join("OST", canciones[cancion_actual]))
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == ALIEN_PORTAL:
                texto_pantalla = "¡Llegaste al portal!"
                pygame.mixer.music.pause()
                random_sound = random.choice(PORTAL_SOUNDS)
                random_sound.play()
                draw_mensaje(texto_pantalla)
                nivel_actual += 1
                cancion_actual +=1
                if nivel_actual < len(csv_files):
                    maze = cargar_nivel(os.path.join("NIVELES", csv_files[nivel_actual]))
                    pygame.mixer.music.load(os.path.join("OST", canciones[cancion_actual]))
                    pygame.mixer.music.play(-1)
                    if not maze:  # Verificar que el laberinto se haya cargado correctamente
                        print("Error: El laberinto está vacío.")
                        run = False  # Termina el juego si hay un error
                else:
                    draw_mensaje("¡Has completado todos los niveles!")
                    pygame.quit()  # Salimos del bucle si se completan todos los niveles
                break

        keys_pressed = pygame.key.get_pressed()
        alien_movement(keys_pressed, alien)
        draw_window(alien)
        
    pygame.quit()


if __name__ == "__main__":
    main()