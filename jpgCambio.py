import os
import shutil

# Ruta a la carpeta que contiene los archivos
ruta_carpeta_origen = r"D:\data\pruebaDatasetInternet"

# Ruta a la carpeta de destino para los archivos modificados
ruta_carpeta_destino = r"D:\data\prueba"

# Crear la carpeta de destino si no existe
if not os.path.exists(ruta_carpeta_destino):
    os.makedirs(ruta_carpeta_destino)

# Obtener la lista de archivos en la carpeta de origen
lista_archivos = os.listdir(ruta_carpeta_origen)

# Iterar sobre los archivos en la carpeta de origen
for archivo in lista_archivos:
    # Obtener la ruta completa del archivo de origen
    ruta_archivo_origen = os.path.join(ruta_carpeta_origen, archivo)

    # Verificar si el archivo tiene la extensión .JPG
    if archivo.lower().endswith(".jpg"):
        # Cambiar la extensión del archivo a .jpg
        nuevo_nombre = os.path.splitext(archivo)[0] + ".jpg"

        # Crear la ruta completa del archivo de destino
        ruta_archivo_destino = os.path.join(ruta_carpeta_destino, nuevo_nombre)

        # Copiar el archivo con la nueva extensión a la carpeta de destino
        shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)
