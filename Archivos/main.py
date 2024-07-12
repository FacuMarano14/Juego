import pygame
from settings import *
from personajes import Personaje
from weapon import Weapon
from weapon import Bullet
import os
from items import Item
from random import randint

def escalar_imagen(imagen, escala):
    w = imagen.get_width()
    h = imagen.get_height()
    nueva_imagen = pygame.transform.scale(imagen, (w*escala, h*escala))
    return nueva_imagen
#----------------------------------------------------------------------------------
def contar_elementos(directorio):
    return len(os.listdir(directorio))
#----------------------------------------------------------------------------------
def nombre_carpetas(directorio):
     return os.listdir(directorio)
#----------------------------------------------------------------------------------
def vida_jugador(jugador):
    cor_mitad_dibuj = False
    for i in range(3):
        if jugador.energia >= ((i+1)*25):
            ventana.blit(corazon_completo, (5+i*50,5))
        elif jugador.energia % 25 > 0 and cor_mitad_dibuj == False:
            ventana.blit(corazon_mitad, (5+i*50,5))
            cor_mitad_dibuj = True
        else:
            ventana.blit(corazon_vacio, (5+i*50,5))
#----------------------------------------------------------------------------------
def dibujar_txt_pantalla(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x,y))
#----------------------------------------------------------------------------------
def pantalla_inicio():
    ventana.fill(MAGENTA)
    dibujar_txt_pantalla("Pedrovich", font_titulo, WHITE, ANCHO_PANTALLA / 2 - 200, ALTO_PANTALLA / 2 - 200)
    pygame.draw.rect(ventana,YELLOW,boton_jugar)
    pygame.draw.rect(ventana,BLUE,boton_opciones)
    pygame.draw.rect(ventana,RED,boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x +43, boton_jugar.y +17))
    ventana.blit(texto_boton_opciones, (boton_opciones.x +30, boton_opciones.y +14))
    ventana.blit(texto_boton_salir, (boton_salir.x +50, boton_salir.y +17))
    pygame.display.update()

#----------------------------------------------------------------------------------
def escalar_fondo(imagen, tamaño):
    return pygame.transform.scale(imagen, tamaño)

pygame.init()
pygame.mixer.init()


#Barra salud
corazon_completo = pygame.image.load("Barra_salud//corazon_completo.png")
corazon_completo = escalar_imagen(corazon_completo, ESCALA_BARRA_VIDA)
corazon_mitad = pygame.image.load("Barra_salud//corazon_mitad.png")
corazon_mitad = escalar_imagen(corazon_mitad, ESCALA_BARRA_VIDA)
corazon_vacio = pygame.image.load("Barra_salud//corazon_vacio.png")
corazon_vacio = escalar_imagen(corazon_vacio, ESCALA_BARRA_VIDA)


#Personaje
animaciones = []
for i in range(6):
    img = pygame.image.load(f"Characters//Correr//adventurer-run-0{i}.png")
    img = escalar_imagen(img, ESCALA_PERSONAJE)
    animaciones.append(img)

#Enemigos
directorio_enemigos = "Enemigos"
tipo_enemigo = nombre_carpetas(directorio_enemigos)
animaciones_enemigos = []
for enem in tipo_enemigo:
    lista_temp = []
    ruta_temp = f"Enemigos//{enem}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        imagen_enemigo = pygame.image.load(f"{ruta_temp}//{enem}_{i+1}.png")
        imagen_enemigo = escalar_imagen(imagen_enemigo, ESCALA_ENEMIGOS)
        lista_temp.append(imagen_enemigo)
    animaciones_enemigos.append(lista_temp)
print(lista_temp)


#Arma
imagen_magnum = pygame.image.load("Weapons//UNSC//magnum.png") 
imagen_magnum = escalar_imagen(imagen_magnum, ESCALA_ARMA)

#Balas
imagen_balas = pygame.image.load("Laser Sprites//01.png")
imagen_balas = escalar_imagen(imagen_balas, ESCALA_BALA)

#Cargar imagenes
posion_1 = pygame.image.load("Items//potion_1.png")
posion_1 = escalar_imagen(posion_1, ESCALA_POSION)

coin = pygame.image.load("Items//coin_3.png")
coin = escalar_imagen(coin, ESCALA_COIN)






        
#Crear jugador clase Personaje
jugador = Personaje(50, 50, animaciones, 00, 0)

# Crear enemigo clase Personaje
caballero = Personaje(randint(0, ANCHO_PANTALLA - ANCHO_PERSONAJE), randint(0,ALTO_PANTALLA - ALTO_PERSONAJE), animaciones_enemigos[0], 75, 1)
esqueleto = Personaje(randint(0, ANCHO_PANTALLA - ANCHO_PERSONAJE), randint(0,ALTO_PANTALLA - ALTO_PERSONAJE), animaciones_enemigos[1], 75, 2)
monstruo = Personaje(randint(0, ANCHO_PANTALLA - ANCHO_PERSONAJE), randint(0,ALTO_PANTALLA - ALTO_PERSONAJE), animaciones_enemigos[2], 75, 3)

lista_enemigos = []
lista_enemigos.append(caballero)
lista_enemigos.append(esqueleto)
lista_enemigos.append(monstruo)




#Crear arma clase WEAPON
magnum = Weapon(imagen_magnum, imagen_balas)


moneda = Item(350,25,0,coin)
posion_1 = Item(380,55,1,posion_1)



#Crear grupo sprites
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

grupo_items.add(moneda)
grupo_items.add(posion_1)

# for _ in range(10):
#     x = randint(0, ANCHO_PANTALLA)
#     y = randint(0, ALTO_PANTALLA)
#     nueva_moneda = Item(x, y, 0, coin)  # Crear una nueva instancia de Item con posiciones aleatorias
#     grupo_items.add(nueva_moneda)


font = pygame.font.Font("Font//PixeloidSans-Bold.ttf", 15)
font_game_over = pygame.font.Font("Font//PixeloidSans-Bold.ttf", 100)
font_reinicio = pygame.font.Font("Font//PixeloidSans-Bold.ttf", 32 )
font_inicio = pygame.font.Font("Font//PixeloidSans-Bold.ttf", 15 )
font_titulo = pygame.font.Font("Font//PixeloidSans-Bold.ttf", 70 )


game_over_txt = font_game_over.render("Game Over", True, BLACK)
texto_boton_menu = font_reinicio.render("Menu", True, BLACK)

boton_jugar = pygame.Rect(ANCHO_PANTALLA / 2 - 100, ALTO_PANTALLA / 2 - 70, 150, 50)
boton_opciones = pygame.Rect(ANCHO_PANTALLA / 2 - 100, ALTO_PANTALLA / 2 + 10, 150, 50)
boton_salir = pygame.Rect(ANCHO_PANTALLA / 2 - 100, ALTO_PANTALLA / 2 + 100, 150, 50)

texto_boton_jugar = font_inicio.render("Jugar", True, BLACK)
texto_boton_opciones = font_inicio.render("Opciones", True, BLACK)
texto_boton_salir = font_inicio.render("Salir", True, BLACK)

fondo = pygame.image.load("Background//fondo.png")
fondo = escalar_fondo(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Videojuego")


#definir variables movimiento
mover_izquierda = False
mover_derecha = False
mover_arriba = False
mover_abajo = False

sonido_disparo = pygame.mixer.Sound("sound effects//Laser.wav")
sonido_moneda = pygame.mixer.Sound("sound effects//Coin.wav")

run = True
mostrar_inicio = True

reloj = pygame.time.Clock()

while run:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
        
    else:
        reloj.tick(FPS)

        ventana.blit(fondo, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False

        if jugador.vivo:
            #calcular movimiento jugador
            delta_x = 0
            delta_y = 0

            jugador.dibujar(ventana)


            if mover_arriba == True:
                delta_y = -VELOCIDAD
            if mover_abajo == True:
                delta_y = VELOCIDAD
            if mover_izquierda == True:
                delta_x = -VELOCIDAD
            if mover_derecha == True:
                delta_x = VELOCIDAD
            

            
            #Mover jugador
            jugador.movimiento(delta_x, delta_y)


            #Actualizar Enemigo
            for ene in lista_enemigos:
                ene.mov_enemigos(jugador)
                ene.update()
                print(ene.energia)

            #Actualiza arma
            bala = magnum.update(jugador)
            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            for bala in grupo_balas:
                bala.update(lista_enemigos)

            #actualizar items
            grupo_items.update(jugador)
            
        
        

        #Dibujar jugador
        jugador.dibujar(ventana)

        #borrar enemigos
        for ene in lista_enemigos[:]:
            if ene.energia == 0:
                lista_enemigos.remove(ene)
            else:
                ene.update()
                ene.dibujar(ventana)
            


        #Dibujar arma
        magnum.dibujar(ventana)

        #Dibujar balas
        for bala in grupo_balas:
            bala.update(lista_enemigos)
            bala.dibujar(ventana)

        #Dibujar vida
        vida_jugador(jugador)


        #dibujar text
        dibujar_txt_pantalla(f"Score: {jugador.score}", font, YELLOW, 700, 5)
        #Actualizar jugador
        jugador.update()

        #dibujar items
        grupo_items.draw(ventana)

        if jugador.vivo == False:
            ventana.fill(RED)
            text_rect = game_over_txt.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 100))
            ventana.blit(game_over_txt, text_rect)
            boton_menu = pygame.Rect(ANCHO_PANTALLA / 2 - 120, ALTO_PANTALLA / 2 + 100, 200, 70)
            pygame.draw.rect(ventana, WHITE, boton_menu)
            ventana.blit(texto_boton_menu, (boton_menu.x +40, boton_menu.y +10))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_menu.collidepoint(event.pos) and not jugador.vivo:
                    jugador.vivo = True
                    jugador.energia = 100
                    jugador.score = 0
                    mostrar_inicio = True

        
            
            
                    
            
        
        pygame.display.update()

pygame.quit()

