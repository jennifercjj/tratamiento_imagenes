import os
import random
import shutil

# Ruta a la carpeta que contiene las imágenes
ruta_imagenes = r"C:\Users\Personal\Desktop\Dataset\Data_Weisner"

# Número de imágenes a seleccionar
num_imagenes = 360

# Obtener la lista de archivos en la carpeta
lista_archivos = os.listdir(ruta_imagenes)

# Filtrar solo los archivos de imagen (por ejemplo, con extensión .jpg)
lista_imagenes = [archivo for archivo in lista_archivos if archivo.endswith(".JPG")]

# Elegir 360 imágenes aleatoriamente
imagenes_seleccionadas = random.sample(lista_imagenes, num_imagenes)

# Carpeta de destino para las imágenes seleccionadas
carpeta_destino = r"D:\data\seleccion_dataset360Original"

# Mover las imágenes seleccionadas a la carpeta de destino
for imagen in imagenes_seleccionadas:
    origen = os.path.join(ruta_imagenes, imagen)
    destino = os.path.join(carpeta_destino, imagen)
    shutil.move(origen, destino)
