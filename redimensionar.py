from PIL import Image
import os

# ruta a la carpeta que contiene las imágenes
ruta = r"D:\data\prueba"

# tamaño deseado
nuevo_tamano = (640, 640)

# iterar sobre todas las imágenes en la carpeta
for imagen in os.listdir(ruta):
    # abrir la imagen
    imagen_abierta = Image.open(os.path.join(ruta, imagen))

    # cambiar el tamaño
    imagen_nueva = imagen_abierta.resize(nuevo_tamano)

    # guardar la imagen con el mismo nombre pero en una carpeta nueva
    carpeta_nueva = r"D:\data\test"
    if not os.path.exists(carpeta_nueva):
        os.makedirs(carpeta_nueva)
    imagen_nueva.save(os.path.join(carpeta_nueva, imagen))
