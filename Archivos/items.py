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
        pygame.sprite.Sprite.__init__(self)  # Inicializar la clase base Sprite
        self.item_type = item_type  # Tipo de ítem: 0 para moneda, 1 para poción
        self.image = image  # Imagen del ítem
        self.rect = self.image.get_rect()  # Obtener el rectángulo de la imagen
        self.rect.center = (x, y)  # Establecer la posición del ítem en la pantalla
        
    def update(self, personaje):
        """Actualiza el estado del ítem, detecta colisiones con el personaje y realiza las acciones correspondientes.

        Args:
            personaje (objeto): El personaje con el que el ítem puede colisionar.
        """
        # Cargar sonidos para los ítems
        sonido_moneda = pygame.mixer.Sound("sound effects//Coin.wav")
        sonido_potion = pygame.mixer.Sound("sound effects//Potion.wav")

        # Verificar si el ítem colisiona con el personaje
        if self.rect.colliderect(personaje.forma):
            if self.item_type == 0:  # Si el ítem es una moneda
                personaje.score += 1  # Aumentar el puntaje del personaje
                sonido_moneda.play()  # Reproducir sonido de moneda
            elif self.item_type == 1:  # Si el ítem es una poción
                personaje.energia += 25  # Aumentar la energía del personaje
                if personaje.energia > 100:  # Asegurarse de que la energía no exceda 100
                    personaje.energia = 100
                sonido_potion.play()  # Reproducir sonido de poción
                # Crear una nueva poción en una posición aleatoria
                x = randint(0, ANCHO_PANTALLA)
                y = randint(0, ALTO_PANTALLA)
                nueva_posion = Item(x, y, 1, self.image)
                self.groups()[0].add(nueva_posion)  # Agregar la nueva poción al grupo de ítems
            self.kill()  # Eliminar el ítem actual