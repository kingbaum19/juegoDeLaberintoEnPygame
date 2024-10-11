import pygame
import json

#~~~~~~~~~~~~~~~~~~~~~~Sprite para insertar en el juego.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Spritesheet:
    def __init__ (self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png' ,'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        
        self.rect = self.sprite_sheet.get_rect()
    
    def get_sprite(self, x,y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey ((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x,y, w, h))
        return sprite
    
        
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x,y,w,h)
        return image
    
    
#~~~~~~~~~~~~~~~~~~instruccion para el codigo principal~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#segun el video se tiene que copiar el comando "" todos los fotogramas(nea)
# este se esta trabajando cin el archivo json

