import pygame
from settings import *
from math import sqrt

class Personaje():
    def __init__(self, x, y, animaciones, energia, tipo):
        self.score = 0
        self.energia = energia
        self.flip = False
        self.vivo = True
        self.animaciones = animaciones
        #imagen de animacion que se muestra actualmente
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
        self.tipo_personaje = tipo
        self.hit = False
        self.ultimo_hit = pygame.time.get_ticks()

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        #pygame.draw.rect(interfaz, COLOR_PERSONAJE, self.forma, 1)
    
    def update(self):
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False


        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
             self.frame_index = self.frame_index + 1
             self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    
    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y
    
    def mov_enemigos(self, personaje):
        ene_dx = 0
        ene_dy = 0
        if self.forma.centerx > personaje.forma.centerx:          
            ene_dx = -VELOCIDAD_ENEMIGO   
        if self.forma.centerx < personaje.forma.centerx:           
            ene_dx = VELOCIDAD_ENEMIGO   
        if self.forma.centery > personaje.forma.centery:
            ene_dy = -VELOCIDAD_ENEMIGO  
        if self.forma.centery < personaje.forma.centery:
            ene_dy = VELOCIDAD_ENEMIGO 
        
        distancia  = sqrt(((self.forma.centerx - personaje.forma.centerx)** 2) + ((self.forma.centery - personaje.forma.centery) ** 2) )

        if distancia < RANGO_ATAQUE_ENEMIGO and personaje.hit == False:
            personaje.energia -= DAÑO_ENEMIGO
            personaje.hit = True
            personaje.ultimo_hit = pygame.time.get_ticks()

        self.movimiento(ene_dx, ene_dy)


    
    
    

    
    
    
    