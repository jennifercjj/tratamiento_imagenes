from PIL import Image
import os
import random
import shutil

# Ruta a la carpeta que contiene las imágenes originales
ruta_imagenes = r"D:\data\Dataset"

# Número de imágenes a seleccionar
num_imagenes = 80
lista_archivos = os.listdir(ruta_imagenes)
lista_imagenes = [archivo for archivo in lista_archivos if (archivo.endswith(".jpg") or archivo.endswith(".JPG")) ]
# Elegir 80 imágenes aleatoriamente
imagenes_seleccionadas = random.sample(lista_imagenes, num_imagenes)
# Carpeta de destino para las imágenes giradas
carpeta_destino = r"D:\data\80imagenesRotacion90"
# Iterar sobre las imágenes seleccionadas, crear copias y rotarlas 90 grados
for imagen in imagenes_seleccionadas:
    origen = os.path.join(ruta_imagenes, imagen)
    imagen_original = Image.open(origen)
    imagen_copia = imagen_original.copy()
    # Rotar la imagen copiada 90 grados en sentido horario
    imagen_rotada = imagen_copia.rotate(-90, expand=True)
    # Obtener el nombre del archivo sin extensión
    nombre_archivo = os.path.splitext(imagen)[0]
    # Crear el nombre del archivo de destino para la imagen girada
    archivo_destino = f"{nombre_archivo}_gira90.jpg"
    ruta_destino = os.path.join(carpeta_destino, archivo_destino)
    imagen_rotada.save(ruta_destino)
    imagen_original.close()
    imagen_copia.close()
