#~~~~~~~~~~~~~~~~~~~~LIBRERÍAS Y MODULOS~~~~~~~~~~~~~~~~~~
import pygame
import random
import os
import csv
from Prueba import Spritesheet
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

#~~~~~~~~~~~~~~~~~~~~TAMAÑO DE LAS CASILLAS Y VENTANA~~~~~~~~~~~~~~~~~~
pygame.init()
TILE_SIZE = 32
ALTO, ANCHO = 512, 512
WIN = pygame.display.set_mode((ANCHO,ALTO), pygame.SCALED | pygame.RESIZABLE) #pygame.SCALED es para que aumente el tamaño de la ventana del juego dependiendo de la resolución de nuestro monitor
                                                                              #pygame.RESIZABLE es para la ventana del juego se muestre en tamaño completo y en modo ventana
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
SUEL0 = pygame.image.load(os.path.join('ASSETS','FLOOR.png'))
CASILLAS = [SUELO,VOID,PORTAL,SPAWN,COIN,SUEL0] #SUEL0 es la superficie que activa la condición del screamer

FILAS = 16
COLUMNAS = 16

ALIEN = pygame.image.load(os.path.join('ASSETS','ALIEN.png')).convert_alpha()
alien = ALIEN.get_rect()

my_spritesheet = Spritesheet(os.path.join('ASSETS', 'sprite_sheet.png'))
gherkin = [my_spritesheet.parse_sprite('frame_0.png'),my_spritesheet.parse_sprite('frame_1.png'),my_spritesheet.parse_sprite('frame_2.png'),my_spritesheet.parse_sprite('frame_3.png'),
           my_spritesheet.parse_sprite('frame_4.png'),my_spritesheet.parse_sprite('frame_5.png'),my_spritesheet.parse_sprite('frame_6.png'),my_spritesheet.parse_sprite('frame_7.png'),
           my_spritesheet.parse_sprite('frame_8.png'),my_spritesheet.parse_sprite('frame_9.png'),my_spritesheet.parse_sprite('frame_10.png'),my_spritesheet.parse_sprite('frame_11.png'),
           my_spritesheet.parse_sprite('frame_12.png'),my_spritesheet.parse_sprite('frame_13.png'),my_spritesheet.parse_sprite('frame_14.png'),my_spritesheet.parse_sprite('frame_15.png'),
           my_spritesheet.parse_sprite('frame_16.png'),my_spritesheet.parse_sprite('frame_17.png'),my_spritesheet.parse_sprite('frame_18.png'),my_spritesheet.parse_sprite('frame_19.png'),
           my_spritesheet.parse_sprite('frame_20.png'),my_spritesheet.parse_sprite('frame_21.png'),my_spritesheet.parse_sprite('frame_22.png'),my_spritesheet.parse_sprite('frame_23.png'),
           my_spritesheet.parse_sprite('frame_24.png'),my_spritesheet.parse_sprite('frame_25.png'),my_spritesheet.parse_sprite('frame_26.png'),my_spritesheet.parse_sprite('frame_27.png'),
           my_spritesheet.parse_sprite('frame_28.png'),my_spritesheet.parse_sprite('frame_29.png'),my_spritesheet.parse_sprite('frame_30.png'),my_spritesheet.parse_sprite('frame_31.png'),
           my_spritesheet.parse_sprite('frame_32.png'),my_spritesheet.parse_sprite('frame_33.png'),my_spritesheet.parse_sprite('frame_34.png'),my_spritesheet.parse_sprite('frame_35.png'),
           my_spritesheet.parse_sprite('frame_36.png'),my_spritesheet.parse_sprite('frame_37.png'),my_spritesheet.parse_sprite('frame_38.png'),my_spritesheet.parse_sprite('frame_39.png'),
           my_spritesheet.parse_sprite('frame_40.png'),my_spritesheet.parse_sprite('frame_41.png'),my_spritesheet.parse_sprite('frame_42.png'),my_spritesheet.parse_sprite('frame_43.png')]
gherkin_index = 0

warrior = pygame.transform.scale(pygame.image.load(os.path.join('ASSETS','warrior.png')), (ANCHO,ALTO)) #Esta es la imagen del screamer
scientific = pygame.image.load(os.path.join('ASSETS', 'SCIENCE.png')) #Esta es la pantalla de muerte

#~~~~~~~~~~~~~~~~~~~~EFECTOS DE SONIDO~~~~~~~~~~~~~~~~~~~~~~~~~~
YAHOO_1 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO1.mp3'))
YAHOO_2 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO2.mp3'))
YAHOO_3 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO3.mp3'))
YAHOO_4 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO4.mp3'))
YAHOO_5 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO5.mp3'))
YAHOO_6 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO6.mp3'))
YAHOO_7 = pygame.mixer.Sound(os.path.join('SONIDO', 'YAHOO7.mp3')) #El efecto de sonido del screamer
YAHOO_8 = pygame.mixer.Sound(os.path.join('SONIDO','YAHOO8.mp3'))
PORTAL_SOUNDS = [YAHOO_1,YAHOO_2,YAHOO_3,YAHOO_4,YAHOO_5,YAHOO_6]

PASOS = pygame.mixer.Sound(os.path.join('SONIDO', 'STEPS.WAV'))
PARED = pygame.mixer.Sound(os.path.join('SONIDO', 'DSOOF.wav'))

canciones = os.listdir("OST")
cancion_actual = 0

#~~~~~~~~~~~~~~~~~~~~~~~~EVENTOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ALIEN_PORTAL = pygame.USEREVENT +1 #El Evento en donde se activa el texto el pantalla y la transición de niveles
ALIEN_FINAL = pygame.USEREVENT +2 #El Evento en donde se activa el screamer

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
            if maze[fila][columna] == 2: #Casilla en donde aparecerá el sprite del pepino
                my_spritesheet.rect.x = columna * TILE_SIZE
                my_spritesheet.rect.y = fila * TILE_SIZE            
    return maze
#Utilizamos archivos .csv para los diseños de niveles porque el programa Tiled Map Editor nos facilita la creación de niveles exportando el resultado final como archivo .csv
csv_files = os.listdir("NIVELES")
nivel_actual = 0
maze = cargar_nivel(os.path.join("NIVELES", csv_files[nivel_actual])) #Se va a formar un laberinto dependiendo de los contenidos de un archivo de la carpeta "NIVELES", y el juego va a formarlos según el valor del iterador

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
    if casilla in [SUELO,PORTAL,COIN, SUEL0]:
        alien.x = columna * TILE_SIZE
        alien.y = fila * TILE_SIZE
    if casilla == VOID:
        PARED.play()
    if casilla == PORTAL:
        pygame.event.post(pygame.event.Event(ALIEN_PORTAL))
    if casilla == SUEL0:
        pygame.event.post(pygame.event.Event(ALIEN_FINAL))

def draw_window(alien,gherkin, gherkin_index):
    for fila in range(len(maze)):
        for columna in range (len(maze[fila])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE
            casilla = CASILLAS[maze[fila][columna]]
            WIN.blit(casilla,(x,y))
    WIN.blit(ALIEN,(alien.x, alien.y))
    WIN.blit(gherkin[gherkin_index], (my_spritesheet.rect.x,my_spritesheet.rect.y))
    pygame.display.update()

def draw_warrior(warrior,cientific): #Esta función es lo que hará que el screamer se muestre en pantalla acompañado de su efecto de sonido
    pygame.mixer.music.pause()
    WIN.fill((0,0,0))
    WIN.blit(warrior,(0,0))
    YAHOO_7.play()
    pygame.display.update()
    pygame.time.delay(3000)
    WIN.blit(cientific,(0,0))
    YAHOO_8.play()
    pygame.display.update()
    pygame.time.delay(7000)
    pygame.quit()


def main ():
    global nivel_actual, maze, cancion_actual, gherkin_index
    pygame.mixer.music.load(os.path.join("OST", canciones[cancion_actual])) #El juego va a reproducir música de un archivo de la carpeta OST según el valor del iterador
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        gherkin_index = (gherkin_index + 1) % len(gherkin) #Esta parte del código hará que el pepino reproduzca sus frames de animación 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == ALIEN_PORTAL:
                texto_pantalla = "¡Llegaste al portal!"
                pygame.mixer.music.pause()
                random_sound = random.choice(PORTAL_SOUNDS)
                random_sound.play()
                draw_mensaje(texto_pantalla)
                nivel_actual += 1 #El iterador pasa al siguiente elemento de la carpeta "NIVELES"
                cancion_actual +=1 #El iterador pasa al siguiente elemento de la carpeta "OST"
                if nivel_actual < len(csv_files):
                    maze = cargar_nivel(os.path.join("NIVELES", csv_files[nivel_actual]))
                    pygame.mixer.music.load(os.path.join("OST", canciones[cancion_actual]))
                    pygame.mixer.music.play(-1)
                else:
                    draw_mensaje("¡Has completado todos los niveles!")
                    pygame.quit() 
                break

            if event.type == ALIEN_FINAL:
                draw_warrior(warrior,scientific)
                        
        keys_pressed = pygame.key.get_pressed()
        alien_movement(keys_pressed, alien)
        draw_window(alien,gherkin, gherkin_index)
        
    pygame.quit()


if __name__ == "__main__":
    main()
