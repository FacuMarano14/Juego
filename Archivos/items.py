import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, image):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    
    def reubicar(self):
        """reubicar
        Reposiciona el item en una ubicación aleatoria en la pantalla.
        """
        self.rect.x = randint(0, ANCHO_PANTALLA)
        self.rect.y = randint(0, ALTO_PANTALLA)

    def update(self, personaje):
        #detectar colidiones
        if self.rect.colliderect(personaje.forma):
            if self.item_type == 0:
                personaje.score += 1
            elif self.item_type == 1:
                personaje.energia += 50
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()