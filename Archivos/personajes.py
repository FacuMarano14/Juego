import pygame
from settings import *
from math import sqrt

class Personaje():
    def __init__(self, x, y, animaciones, energia, tipo):
        """
        Inicializa un objeto Personaje.

        Args:
            x (int): Coordenada x inicial del personaje.
            y (int): Coordenada y inicial del personaje.
            animaciones (list): Lista de imágenes de animación para el personaje.
            energia (int): Energía inicial del personaje.
            tipo (str): Tipo de personaje (ej. jugador, enemigo).
        """
        self.score = 0  # Puntaje del personaje
        self.energia = energia  # Energía del personaje
        self.flip = False  # Indica si la imagen del personaje está volteada horizontalmente
        self.vivo = True  # Indica si el personaje está vivo
        self.animaciones = animaciones  # Lista de imágenes de animación
        self.frame_index = 0  # Índice del frame de animación actual
        self.update_time = pygame.time.get_ticks()  # Tiempo de la última actualización de animación
        self.image = animaciones[self.frame_index]  # Imagen actual del personaje
        self.forma = self.image.get_rect()  # Rectángulo que representa la forma del personaje
        self.forma.center = (x, y)  # Posición inicial del personaje
        self.tipo_personaje = tipo  # Tipo de personaje (jugador o enemigo)
        self.ultimo_hit = pygame.time.get_ticks()  # Tiempo del último golpe recibido
        self.cooldown_ataque = 1000  # Tiempo de espera entre ataques (en milisegundos)
        self.ultimo_ataque = pygame.time.get_ticks()  # Tiempo del último ataque realizado

    def dibujar(self, interfaz):
        """
        Dibuja el personaje en la interfaz proporcionada.

        Args:
            interfaz (pygame.Surface): La superficie en la que se dibuja el personaje.
        """
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)  # Voltea la imagen si es necesario
        interfaz.blit(imagen_flip, self.forma)  # Dibuja la imagen del personaje en la interfaz
        # pygame.draw.rect(interfaz, COLOR_PERSONAJE, self.forma, 1)  # Dibuja el rectángulo del personaje (para depuración)

    def update(self):
        """
        Actualiza el estado del personaje, verificando su energía y manejando la animación.
        """
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False  # Si la energía es 0 o menos, el personaje está muerto

        cooldown_animacion = 100  # Tiempo de espera entre frames de animación
        self.image = self.animaciones[self.frame_index]  # Actualiza la imagen del personaje
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1  # Cambia al siguiente frame de animación
            self.update_time = pygame.time.get_ticks()  # Actualiza el tiempo de la última animación
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0  # Vuelve al primer frame si ha llegado al final de la lista

    def movimiento(self, delta_x, delta_y):
        """
        Mueve el personaje según los desplazamientos dados y limita su movimiento a los bordes de la pantalla.

        Args:
            delta_x (int): Desplazamiento en el eje x.
            delta_y (int): Desplazamiento en el eje y.
        """
        if delta_x < 0:
            self.flip = True  # Voltea la imagen si se mueve hacia la izquierda
        if delta_x > 0:
            self.flip = False  # No voltea la imagen si se mueve hacia la derecha

        # Calcular nuevas posiciones
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
        """
        Mueve al enemigo hacia el personaje y maneja los ataques del enemigo.

        Args:
            personaje (Personaje): El personaje objetivo del enemigo.
        """
        ene_dx = 0  # Desplazamiento del enemigo en el eje x
        ene_dy = 0  # Desplazamiento del enemigo en el eje y
        if self.forma.centerx > personaje.forma.centerx:          
            ene_dx = -VELOCIDAD_ENEMIGO  # Mueve el enemigo hacia la izquierda
        if self.forma.centerx < personaje.forma.centerx:           
            ene_dx = VELOCIDAD_ENEMIGO  # Mueve el enemigo hacia la derecha
        if self.forma.centery > personaje.forma.centery:
            ene_dy = -VELOCIDAD_ENEMIGO  # Mueve el enemigo hacia arriba
        if self.forma.centery < personaje.forma.centery:
            ene_dy = VELOCIDAD_ENEMIGO  # Mueve el enemigo hacia abajo
        
        distancia = sqrt(((self.forma.centerx - personaje.forma.centerx) ** 2) + ((self.forma.centery - personaje.forma.centery) ** 2))  # Calcula la distancia entre el enemigo y el personaje

        if distancia < RANGO_ATAQUE_ENEMIGO:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_ataque >= self.cooldown_ataque:
                personaje.energia -= DAÑO_ENEMIGO  # Reduce la energía del personaje si el enemigo está en rango de ataque
                self.ultimo_ataque = ahora  # Actualizar el tiempo del último ataque

        self.movimiento(ene_dx, ene_dy)  # Mueve al enemigo hacia el personaje




