import pygame
from settings import *
from math import degrees, atan2, cos, radians, sin
from personajes import Personaje
from random import randint

class Weapon():
    def __init__(self, image, imagen_bala):
        """Inicializa un objeto Weapon.

        Args:
            image (pygame.Surface): Imagen del arma.
            imagen_bala (pygame.Surface): Imagen de la bala disparada por el arma.
        """
        # Imagen del arma y de la bala
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0  # Ángulo de rotación del arma
        self.imagen = self.imagen_original.copy()  # Copia de la imagen original del arma
        self.forma = self.imagen.get_rect()  # Rectángulo que define el área del arma
        self.disparada = False  # Estado de si el arma ha disparado o no
        self.ultimo_disparo = pygame.time.get_ticks()  # Tiempo del último disparo
    
    def rotar_arma(self, rotar):
        """Rota la imagen del arma según la dirección del personaje.

        Args:
            rotar (bool): Indica si la imagen del arma debe ser rotada.
        """
        if rotar:
            # Rotar la imagen del arma y voltear horizontalmente
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            # Rotar la imagen del arma sin voltear
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
    
    def update(self, personaje):
        """Actualiza la posición y la rotación del arma, y gestiona los disparos.

        Args:
            personaje (Personaje): El personaje que sostiene el arma.

        Returns:
            Bullet: Una nueva bala disparada, si corresponde; de lo contrario, None.
        """
        disparo_cooldown = COOLDOWN_BALAS  # Tiempo de recarga entre disparos
        bala = None  # Inicializar variable de bala como None
        self.forma.center = personaje.forma.center  # Posicionar el arma en el centro del personaje

        # Ajustar la posición del arma basada en la dirección del personaje
        if personaje.flip:
            # Si el personaje está mirando hacia la izquierda, ajustar posición y rotar
            self.forma.x -= 30
            self.forma.y += 13
            self.rotar_arma(True)
        else:
            # Si el personaje está mirando hacia la derecha, ajustar posición y rotar
            self.forma.x += 30
            self.forma.y += 13
            self.rotar_arma(False)

        # Obtener la posición del mouse para rotar el arma hacia el cursor
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = degrees(atan2(distancia_y, distancia_x))

        # Rotar la imagen del arma según el ángulo calculado
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        if personaje.flip:
            self.imagen = pygame.transform.flip(self.imagen, True, False)
        self.forma = self.imagen.get_rect(center=self.forma.center)  # Actualizar el rectángulo del arma

        # Detectar clics del mouse para disparar
        if pygame.mouse.get_pressed()[0] and not self.disparada and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            # Crear una nueva bala si se cumple el tiempo de recarga
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()
        if not pygame.mouse.get_pressed()[0]:
            self.disparada = False
        return bala

    def dibujar(self, interfaz):
        """Dibuja el arma en la interfaz proporcionada.

        Args:
            interfaz (pygame.Surface): La superficie en la que se dibuja el arma.
        """
        interfaz.blit(self.imagen, self.forma)  # Dibujar el arma en la interfaz
        # pygame.draw.rect(interfaz, COLOR_ARMA, self.forma, 1)  # Opcional: dibujar el contorno del arma

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        """Inicializa un objeto Bullet.

        Args:
            image (pygame.Surface): Imagen de la bala.
            x (int): Coordenada x inicial de la bala.
            y (int): Coordenada y inicial de la bala.
            angle (float): Ángulo de disparo de la bala.
        """
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)  # Rotar la imagen de la bala
        self.rect = self.image.get_rect(center=(x, y))  # Rectángulo que define el área de la bala
        # Calcular el desplazamiento de la bala en función de su ángulo
        self.delta_x = cos(radians(self.angulo)) * VELOCIDAD_BALA
        self.delta_y = -sin(radians(self.angulo)) * VELOCIDAD_BALA
        
    def update(self, lista_enemigos):
        """Actualiza la posición de la bala y verifica colisiones con enemigos.

        Args:
            lista_enemigos (list): Lista de enemigos en el juego.
        """
        self.rect.x += self.delta_x  # Actualizar la posición en x
        self.rect.y += self.delta_y  # Actualizar la posición en y
        # Verificar si la bala ha salido de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA or self.rect.bottom < 0 or self.rect.top > ALTO_PANTALLA:
            self.kill()  # Destruir la bala si sale de la pantalla
        
        # Verificar colisiones con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                # Aplicar daño al enemigo y destruir la bala
                daño = 15 + randint(-7, 7)
                enemigo.energia -= daño
                self.kill()
                break

    def dibujar(self, interfaz):
        """Dibuja la bala en la interfaz proporcionada.

        Args:
            interfaz (pygame.Surface): La superficie en la que se dibuja la bala.
        """
        # Dibujar la bala en la interfaz, centrada en su posición
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/2)))