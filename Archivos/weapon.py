import pygame
from settings import *
from math import degrees, atan2, cos, radians, sin
from personajes import Personaje
from random import randint

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = self.imagen_original.copy()
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.ultimo_disparo = pygame.time.get_ticks()
    
    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
    
    def update(self, personaje):
        disparo_cooldown = COOLDOWN_BALAS
        bala = None
        self.forma.center = personaje.forma.center
        
    


        # Ajustar la posición del arma basada en la dirección del personaje
        if personaje.flip:
            self.forma.x -= 30
            self.forma.y += 13
            self.rotar_arma(True)
        else:
            self.forma.x += 30
            self.forma.y += 13
            self.rotar_arma(False)

        # Mover pistola con mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = degrees(atan2(distancia_y, distancia_x))

        # Rotar la imagen de la pistola
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        if personaje.flip:
            self.imagen = pygame.transform.flip(self.imagen, True, False)
        self.forma = self.imagen.get_rect(center=self.forma.center)

        # Detectar clicks mouse
        if pygame.mouse.get_pressed()[0] and not self.disparada and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()
        if not pygame.mouse.get_pressed()[0]:
            self.disparada = False
        return bala

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, COLOR_ARMA, self.forma, 1)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect(center=(x, y))
        self.delta_x = cos(radians(self.angulo)) * VELOCIDAD_BALA
        self.delta_y = -sin(radians(self.angulo)) * VELOCIDAD_BALA
        
    def update(self, lista_enemigos):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        # Ver si las balas salieron de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA or self.rect.bottom < 0 or self.rect.top > ALTO_PANTALLA:
            self.kill()
        
        # Verificar si hay colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = 15 + randint(-7, 7)
                enemigo.energia -= daño
                self.kill()
                break

    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/2)))

