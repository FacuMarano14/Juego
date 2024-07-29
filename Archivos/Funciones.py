import pygame
from settings import *
import os
from random import randint
import json
import csv
from items import Item
from personajes import Personaje

def escalar_imagen(imagen, escala):
    """Escala una imagen según el factor de escala proporcionado.

    Args:
        imagen (pygame.Surface): La superficie de la imagen a escalar.
        escala (float): Factor por el cual se escalará la imagen.

    Returns:
        pygame.Surface: La nueva superficie de la imagen escalada.
    """
    w = imagen.get_width()
    h = imagen.get_height()
    nueva_imagen = pygame.transform.scale(imagen, (w*escala, h*escala))
    return nueva_imagen
#----------------------------------------------------------------------------------
def contar_elementos(directorio):
    """Cuenta el número de elementos en un directorio.

    Args:
        directorio (str): La ruta al directorio cuyo contenido se va a contar.

    Returns:
        int: Número de elementos en el directorio.
    """
    return len(os.listdir(directorio))
#----------------------------------------------------------------------------------
def nombre_carpetas(directorio):
    """Obtiene una lista de los nombres de las carpetas en un directorio.

    Args:
        directorio (str): La ruta al directorio del cual obtener los nombres de las carpetas.

    Returns:
        list: Lista de nombres de las carpetas en el directorio.
    """
    return os.listdir(directorio)
#----------------------------------------------------------------------------------
def vida_jugador(jugador, ventana, corazon_completo, corazon_mitad, corazon_vacio):
    """Dibuja los iconos de la vida del jugador en la ventana.

    Args:
        jugador (objeto): El objeto jugador que contiene la energía actual.
        ventana (pygame.Surface): La superficie de la ventana donde se dibujarán los iconos de vida.
        corazon_completo (pygame.Surface): Imagen del corazón completo.
        corazon_mitad (pygame.Surface): Imagen del corazón a mitad.
        corazon_vacio (pygame.Surface): Imagen del corazón vacío.
    """
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
def dibujar_txt_pantalla(texto, fuente, color, x, y, ventana):
    """Dibuja un texto en la ventana en las coordenadas especificadas.

    Args:
        texto (str): El texto a dibujar.
        fuente (pygame.font.Font): La fuente del texto.
        color (tuple): Color del texto en formato RGB.
        x (int): Coordenada x para dibujar el texto.
        y (int): Coordenada y para dibujar el texto.
        ventana (pygame.Surface): La superficie de la ventana donde se dibujará el texto.
    """
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x,y))
#----------------------------------------------------------------------------------
def pantalla_inicio(ventana, fondo_inicio, font_titulo, boton_jugar, boton_opciones, boton_salir, texto_boton_jugar, texto_boton_opciones, texto_boton_salir):
    """Dibuja la pantalla de inicio del juego con los botones y el título.

    Args:
        ventana (pygame.Surface): La superficie de la ventana donde se dibujará la pantalla de inicio.
        fondo_inicio (pygame.Surface): Imagen de fondo para la pantalla de inicio.
        font_titulo (pygame.font.Font): Fuente para el título del juego.
        boton_jugar (pygame.Rect): Rectángulo que representa el botón de jugar.
        boton_opciones (pygame.Rect): Rectángulo que representa el botón de opciones.
        boton_salir (pygame.Rect): Rectángulo que representa el botón de salir.
        texto_boton_jugar (pygame.Surface): Texto para el botón de jugar.
        texto_boton_opciones (pygame.Surface): Texto para el botón de opciones.
        texto_boton_salir (pygame.Surface): Texto para el botón de salir.
    """
    ventana.blit(fondo_inicio, (0,0))
    dibujar_txt_pantalla("Pedrovich", font_titulo, WHITE, ANCHO_PANTALLA / 2 - 230, ALTO_PANTALLA / 2 - 200, ventana)
    pygame.draw.rect(ventana,YELLOW,boton_jugar)
    pygame.draw.rect(ventana,BLUE,boton_opciones)
    pygame.draw.rect(ventana,RED,boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x +43, boton_jugar.y +17))
    ventana.blit(texto_boton_opciones, (boton_opciones.x +30, boton_opciones.y +14))
    ventana.blit(texto_boton_salir, (boton_salir.x +50, boton_salir.y +17))
    pygame.display.update()

#----------------------------------------------------------------------------------
def escalar_fondo(imagen, tamaño):
    """Escala una imagen de fondo al tamaño especificado.

    Args:
        imagen (pygame.Surface): La superficie de la imagen a escalar.
        tamaño (tuple): El nuevo tamaño de la imagen en formato (ancho, alto).

    Returns:
        pygame.Surface: La superficie de la imagen escalada.
    """
    return pygame.transform.scale(imagen, tamaño)
#----------------------------------------------------------------------------------
def regenerar_monedas(grupo_items, num_monedas, image):
    """Regenera un número específico de monedas en posiciones aleatorias y las añade a un grupo de ítems.

    Args:
        grupo_items (pygame.sprite.Group): El grupo de ítems al que se añadirán las nuevas monedas.
        num_monedas (int): Número de monedas a generar.
        image (pygame.Surface): Imagen de la moneda.
    """
    for _ in range(num_monedas):
        x = randint(0, ANCHO_PANTALLA)
        y = randint(0, ALTO_PANTALLA)
        nueva_moneda = Item(x, y, 0, image)
        grupo_items.add(nueva_moneda)
#----------------------------------------------------------------------------------
def regenerar_enemigos(lista_enemigos, animaciones_enemigos):
    """Regenera enemigos si la lista de enemigos está vacía.

    Args:
        lista_enemigos (list): Lista donde se añadirán los nuevos enemigos.
        animaciones_enemigos (list): Lista de animaciones para los enemigos.
    """
    if not lista_enemigos:
        tipos_enemigos = len(animaciones_enemigos)
        for i in range(tipos_enemigos):
            nuevo_enemigo = Personaje(randint(0, ANCHO_PANTALLA - ANCHO_PERSONAJE),
                                      randint(0, ALTO_PANTALLA - ALTO_PERSONAJE),
                                      animaciones_enemigos[i], 75, i+1)
            lista_enemigos.append(nuevo_enemigo)

#----------------------------------------------------------------------------------
def regenerar_pociones(grupo_items, num_pociones, image):
    """Regenera un número específico de pociones en posiciones aleatorias y las añade a un grupo de ítems.

    Args:
        grupo_items (pygame.sprite.Group): El grupo de ítems al que se añadirán las nuevas pociones.
        num_pociones (int): Número de pociones a generar.
        image (pygame.Surface): Imagen de la poción.
    """
    for _ in range(num_pociones):
        x = randint(0, ANCHO_PANTALLA)
        y = randint(0, ALTO_PANTALLA)
        nueva_pocion = Item(x, y, 1, image)
        grupo_items.add(nueva_pocion)
#----------------------------------------------------------------------------------
def guardar_rutas_json(rutas, nombre_archivo):
    """guardar_rutas_json

    Args:
        rutas (type): una lista que queremos guardar en el json
        nombre_archivo (type): El nombre del archivo JSON donde se guardarán las rutas.

    """
    with open(nombre_archivo, 'w') as archivo:
        json.dump(rutas, archivo, indent=4)

#----------------------------------------------------------------------------------
def menu_opciones2(ventana, fondo_opciones, fuente_titulo, ANCHO, ALTO, boton_subir_volumen, boton_bajar_volumen, boton_volver, texto_boton_subir_volumen, texto_boton_bajar_volumen, texto_boton_volver, fuente_inicio, volume):
    """Dibuja la pantalla de opciones del juego con botones para ajustar el volumen y volver.

    Args:
        ventana (pygame.Surface): La superficie de la ventana donde se dibujará la pantalla de opciones.
        fondo_opciones (pygame.Surface): Imagen de fondo para la pantalla de opciones.
        fuente_titulo (pygame.font.Font): Fuente para el título de la pantalla de opciones.
        ANCHO (int): Ancho de la ventana del juego.
        ALTO (int): Alto de la ventana del juego.
        boton_subir_volumen (pygame.Rect): Rectángulo que representa el botón de subir volumen.
        boton_bajar_volumen (pygame.Rect): Rectángulo que representa el botón de bajar volumen.
        boton_volver (pygame.Rect): Rectángulo que representa el botón de volver al menú anterior.
        texto_boton_subir_volumen (pygame.Surface): Texto para el botón de subir volumen.
        texto_boton_bajar_volumen (pygame.Surface): Texto para el botón de bajar volumen.
        texto_boton_volver (pygame.Surface): Texto para el botón de volver al menú anterior.
        fuente_inicio (pygame.font.Font): Fuente para el texto del volumen.
        volume (float): Volumen actual del juego.

    Returns:
        float: El volumen actual del juego.
    """
    ventana.blit(fondo_opciones, (0,0))
    dibujar_txt_pantalla("Opciones", fuente_titulo, WHITE, ANCHO/2 - 200, ALTO/2 - 200, ventana)
    pygame.draw.rect(ventana, WHITE, boton_subir_volumen)
    pygame.draw.rect(ventana, WHITE, boton_bajar_volumen)
    pygame.draw.rect(ventana, WHITE, boton_volver)
    ventana.blit(texto_boton_subir_volumen, (boton_subir_volumen.x + 20, boton_subir_volumen.y + 10))
    ventana.blit(texto_boton_bajar_volumen, (boton_bajar_volumen.x + 20, boton_bajar_volumen.y + 10))
    ventana.blit(texto_boton_volver, (boton_volver.x + 55, boton_volver.y + 10))
    dibujar_txt_pantalla(f"Volumen: {int(volume * 100)}%", fuente_inicio, WHITE, ANCHO/2 - 75, ALTO/2 + 150, ventana)
    pygame.display.update()

    return volume
#---------------------------------------------------------------------------------------------------------------------------------
def guardar_usuario_2(nombre, puntaje, usuarios, archivo_csv):
    """Guarda los datos de un usuario en un archivo CSV, añadiéndolos si no están presentes.

    Args:
        nombre (str): Nombre del usuario.
        puntaje (int): Puntaje del usuario.
        usuarios (list): Lista de usuarios donde se añadirá el nuevo usuario si no está presente.
        archivo_csv (str): Nombre del archivo CSV donde se guardarán los datos.

    Returns:
        list: Lista actualizada de usuarios.
    """
    usuario_guardado = False  # Variable local para controlar si se ha guardado el usuario

    # Verificar si el usuario ya está en la lista
    for usuario in usuarios:
        if usuario['nombre'] == nombre:
            # Si el usuario ya existe, marcar como guardado y salir
            usuario_guardado = True
            break

    # Si el usuario no está en la lista, agregarlo
    if not usuario_guardado:
        usuarios.append({
            'nombre': nombre,
            'puntaje': puntaje
        })

        # Verificar si el archivo CSV existe y escribir el encabezado si es nuevo
        escribir_encabezado = not os.path.exists(archivo_csv)

        # Escribir el usuario en el archivo CSV
        with open(archivo_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            if escribir_encabezado:
                writer.writerow(['Nombre', 'Puntaje']) #Encabezado del archivo CSV
            writer.writerow([nombre, puntaje])


    # Retornar la lista actualizada de usuarios (aunque en Python no es necesario, ya que las listas se pasan por referencia)
    return usuarios
#----------------------------------------------------------------------------------
def pantalla_usuario(ventana, fondo_usuario, fuente_inicio, user_text,fuente_inicio_txt,fuente_titulo,cuadro_texto_usuario,boton_ingresar):
    """Muestra la pantalla de ingreso del nombre de usuario.

    Args:
        ventana (pygame.Surface): Superficie de la ventana donde se dibujará la pantalla.
        fondo_usuario (pygame.Surface): Imagen de fondo para la pantalla de usuario.
        fuente_inicio (pygame.font.Font): Fuente para el texto del nombre de usuario.
        user_text (str): Texto actual ingresado por el usuario.
        fuente_inicio_txt (pygame.Surface): Texto para el botón de ingresar.
        fuente_titulo (pygame.font.Font): Fuente para el título de la pantalla.
        cuadro_texto_usuario (pygame.Rect): Rectángulo del cuadro de texto para el usuario.
        boton_ingresar (pygame.Rect): Rectángulo del botón de ingresar.
    """
    ventana.blit(fondo_usuario, (0,0))
    dibujar_txt_pantalla("Ingrese su nombre:", fuente_titulo, WHITE, ANCHO_PANTALLA / 2 - 250,ALTO_PANTALLA / 2 - 200, ventana)
    pygame.draw.rect(ventana, WHITE, cuadro_texto_usuario)
    pygame.draw.rect(ventana, WHITE, boton_ingresar)
    ventana.blit(fuente_inicio_txt, (boton_ingresar.x + 55, boton_ingresar.y + 10))
    dibujar_txt_pantalla(user_text, fuente_inicio, BLACK, cuadro_texto_usuario.x + 5,cuadro_texto_usuario.y + 5, ventana)
    pygame.display.update()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

