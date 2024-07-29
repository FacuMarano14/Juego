import pygame
from settings import *


class Item(pygame.sprite.Sprite):
    """
    Clase para representar un ítem en el juego, que puede ser una moneda o una poción.
    Hereda de pygame.sprite.Sprite para integrar con el sistema de sprites de Pygame.
    """
    def __init__(self, x, y, item_type, image):
        """Inicializa el ítem con su posición, tipo e imagen.

        Args:
            x (int): Coordenada x de la posición del ítem.
            y (int): Coordenada y de la posición del ítem.
            item_type (int): Tipo de ítem (0 para moneda, 1 para poción).
            image (pygame.Surface): Imagen del ítem.
        """
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def update(self, personaje):
        """Actualiza el estado del ítem, detecta colisiones con el personaje y realiza las acciones correspondientes.

        Args:
            personaje (objeto): El personaje con el que el ítem puede colisionar.
        """
        #detectar colisiones
        sonido_moneda = pygame.mixer.Sound("sound effects//Coin.wav")
        sonido_potion = pygame.mixer.Sound("sound effects//Potion.wav")
        if self.rect.colliderect(personaje.forma):
            if self.item_type == 0:  # Moneda
                personaje.score += 1
                sonido_moneda.play()
            elif self.item_type == 1:  # Poción
                personaje.energia += 25
                if personaje.energia > 100:
                    personaje.energia = 100
                sonido_potion.play()
                # Reaparecer poción
                x = randint(0, ANCHO_PANTALLA)
                y = randint(0, ALTO_PANTALLA)
                nueva_posion = Item(x, y, 1, self.image)
                self.groups()[0].add(nueva_posion)
            self.kill()

    # def update(self, personaje):
    #     #detectar colisiones
    #     sonido_moneda = pygame.mixer.Sound("sound effects//Coin.wav")
    #     sonido_potion = pygame.mixer.Sound("sound effects//Potion.wav")
    #     if self.rect.colliderect(personaje.forma):
    #         if self.item_type == 0:
    #             personaje.score += 1
    #             sonido_moneda.play()
    #         elif self.item_type == 1:
    #             personaje.energia += 50
    #             if personaje.energia > 100:
    #                 personaje.energia = 100
                
    #         self.kill()

    

        
                
            