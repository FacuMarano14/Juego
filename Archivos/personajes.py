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
        # self.hit = False
        self.ultimo_hit = pygame.time.get_ticks()
        self.ultimo_hit = pygame.time.get_ticks()
        self.cooldown_ataque = 1000  # Cooldown de 1 segundo (1000 ms)
        self.ultimo_ataque = pygame.time.get_ticks()  # Tiempo del último ataque


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

        #Calcular nuevas posiciones
        nueva_x = self.forma.x + delta_x
        nueva_y = self.forma.y + delta_y

        # Limitar el movimiento a los bordes de la pantalla
        if nueva_x < 0:
            nueva_x = 0
        elif nueva_x > ANCHO_PANTALLA - self.forma.width:
            nueva_x = ANCHO_PANTALLA - self.forma.width

        if nueva_y < 0:
            nueva_y = 0
        elif nueva_y > ALTO_PANTALLA - self.forma.height:
            nueva_y = ALTO_PANTALLA - self.forma.height

        # Actualizar la posición
        self.forma.x = nueva_x
        self.forma.y = nueva_y


    
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

        if distancia < RANGO_ATAQUE_ENEMIGO:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_ataque >= self.cooldown_ataque:
                personaje.energia -= DAÑO_ENEMIGO
                self.ultimo_ataque = ahora  # Actualizar el tiempo del último ataque
        self.movimiento(ene_dx, ene_dy)


# class Personaje():
#     def __init__(self, x, y, animaciones, energia, tipo):
#         self.score = 0
#         self.energia = energia
#         self.flip = False
#         self.vivo = True
#         self.animaciones = animaciones
#         self.frame_index = 0
#         self.update_time = pygame.time.get_ticks()
#         self.image = animaciones[self.frame_index]
#         self.forma = self.image.get_rect()
#         self.forma.center = (x, y)
#         self.tipo_personaje = tipo
#         self.hit = False
#         self.ultimo_hit = pygame.time.get_ticks()
#         self.cooldown_ataque = 1000  # Cooldown de 1 segundo (1000 ms)
#         self.ultimo_ataque = pygame.time.get_ticks()  # Tiempo del último ataque

#     def dibujar(self, interfaz):
#         imagen_flip = pygame.transform.flip(self.image, self.flip, False)
#         interfaz.blit(imagen_flip, self.forma)
    
#     def update(self):
#         if self.energia <= 0:
#             self.energia = 0
#             self.vivo = False

#         cooldown_animacion = 100
#         self.image = self.animaciones[self.frame_index]
#         if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
#             self.frame_index = self.frame_index + 1
#             self.update_time = pygame.time.get_ticks()
#         if self.frame_index >= len(self.animaciones):
#             self.frame_index = 0

#     def movimiento(self, delta_x, delta_y):
#         if delta_x < 0:
#             self.flip = True
#         if delta_x > 0:
#             self.flip = False

#         # Calcular nuevas posiciones
#         nueva_x = self.forma.x + delta_x
#         nueva_y = self.forma.y + delta_y

#         # Limitar el movimiento a los bordes de la pantalla
#         if nueva_x < 0:
#             nueva_x = 0
#         elif nueva_x > ANCHO_PANTALLA - self.forma.width:
#             nueva_x = ANCHO_PANTALLA - self.forma.width

#         if nueva_y < 0:
#             nueva_y = 0
#         elif nueva_y > ALTO_PANTALLA - self.forma.height:
#             nueva_y = ALTO_PANTALLA - self.forma.height

#         # Actualizar la posición
#         self.forma.x = nueva_x
#         self.forma.y = nueva_y

#     def mov_enemigos(self, personaje):
#         ene_dx = 0
#         ene_dy = 0
#         if self.forma.centerx > personaje.forma.centerx:          
#             ene_dx = -VELOCIDAD_ENEMIGO   
#         if self.forma.centerx < personaje.forma.centerx:           
#             ene_dx = VELOCIDAD_ENEMIGO   
#         if self.forma.centery > personaje.forma.centery:
#             ene_dy = -VELOCIDAD_ENEMIGO  
#         if self.forma.centery < personaje.forma.centery:
#             ene_dy = VELOCIDAD_ENEMIGO 
        
#         distancia  = sqrt(((self.forma.centerx - personaje.forma.centerx)** 2) + ((self.forma.centery - personaje.forma.centery) ** 2) )

#         if distancia < RANGO_ATAQUE_ENEMIGO:
#             ahora = pygame.time.get_ticks()
#             if ahora - self.ultimo_ataque >= self.cooldown_ataque:
#                 personaje.energia -= DAÑO_ENEMIGO
#                 self.ultimo_ataque = ahora  # Actualizar el tiempo del último ataque

#         self.movimiento(ene_dx, ene_dy)

