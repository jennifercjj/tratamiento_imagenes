import cv2
import glob
import os
import random
import numpy as np
from skimage.util import random_noise
from PIL import Image, ImageEnhance, ImageFilter


class Data_Augmentation:
    def __init__(self, carpeta_imagenes, carpeta_etiquetas, nueva_carpeta_imagenes, nueva_carpeta_etiquetas):
        self.dataset = []
        self.operations = []
        self.augmented_dataset = []
        self.image_folder = carpeta_imagenes
        self.label_folder = carpeta_etiquetas
        self.new_image_folder = nueva_carpeta_imagenes
        self.new_label_folder = nueva_carpeta_etiquetas

    def load_data(self):
        image_files = glob.glob(os.path.join(self.image_folder, "*.jpg"))
        selected_files = random.sample(image_files, 250)
        for image_file in selected_files:
            data = {}
            img_name = os.path.splitext(os.path.basename(image_file))[0]
            label_file = os.path.join(self.label_folder, img_name + ".txt")
            if os.path.exists(label_file):
                data["image"] = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
                data["bounding_boxes"] = self.load_label(label_file)
                self.dataset.append(data)


    def load_label(self, label_file):
        labels = []
        with open(label_file) as f:
            for line in f:
                data_inline = line.split(" ")
                label = {
                    "class": int(data_inline[0]),
                    "x_center": float(data_inline[1]),
                    "y_center": float(data_inline[2]),
                    "width": float(data_inline[3]),
                    "height": float(data_inline[4][:-1])
                }
                labels.append(label)
        return labels

    def run(self, n_proceso):
        if len(self.dataset) < n_proceso:
            raise ValueError("El conjunto de datos debe tener al menos 5 imágenes para el procesamiento.")

        operations = [
            self.ruido,
            self.brillo,
            self.contraste,
            self.saturacion,
            self.girar_180,
            self.voltear_horizontal

        ]

        for data in self.dataset:
            # Crear una lista temporal para almacenar las imágenes aumentadas de la imagen actual
            augmented_images = []

            for operation in operations:
                new_data = operation(data)
                augmented_images.append(new_data)

            # Agregar las imágenes aumentadas de la imagen actual al conjunto de datos aumentado
            self.augmented_dataset.extend(augmented_images)

    def save_data(self):
        if not os.path.exists(self.new_image_folder):
            os.makedirs(self.new_image_folder)
        if not os.path.exists(self.new_label_folder):
            os.makedirs(self.new_label_folder)

        for i, data in enumerate(self.augmented_dataset):
            image_file = os.path.join(self.new_image_folder, "IMG_{}.jpg".format(i))
            label_file = os.path.join(self.new_label_folder, "IMG_{}.txt".format(i))

            cv2.imwrite(image_file, cv2.cvtColor(data["image"], cv2.COLOR_RGB2BGR))
            self.save_label(label_file, data["bounding_boxes"])

    def save_label(self, label_file, labels):
        with open(label_file, "w") as f:
            for label in labels:
                line = "{} {} {} {} {}\n".format(
                    label["class"],
                    label["x_center"],
                    label["y_center"],
                    label["width"],
                    label["height"]
                )
                f.write(line)

    def ruido(self, data):
        new_data = {}
        src = data["image"]
        noise_img = random_noise(src, mode="gaussian",var=0.07)  # Generar ruido gaussiano con varianza 0.01 (ajustar según sea necesario)
        noisy_image = np.array(255 * noise_img, dtype="uint8")
        noisy_image = cv2.addWeighted(src, 0.8, noisy_image, 0.2, 0)  # Combinar imagen original y el ruido
        new_data["image"] = noisy_image
        new_data["bounding_boxes"] = data["bounding_boxes"]
        return new_data

    def girar_180(self, data):
        new_data = {}
        image = data["image"]
        bbs = data["bounding_boxes"]

        # Girar la imagen 180 grados en sentido horario
        rotated_image = cv2.rotate(image, cv2.ROTATE_180)

        # Ajustar las coordenadas de las etiquetas
        rotated_bbs = []
        for bb in bbs:
            x_center = bb["x_center"]
            y_center = bb["y_center"]
            width = bb["width"]
            height = bb["height"]

            # Calcular las nuevas coordenadas después de la rotación
            x_center_new = 1.0 - x_center
            y_center_new = 1.0 - y_center

            # Crear la nueva etiqueta con las coordenadas ajustadas
            rotated_bb = {
                "class": bb["class"],
                "x_center": x_center_new,
                "y_center": y_center_new,
                "width": width,
                "height": height
            }

            rotated_bbs.append(rotated_bb)

        new_data["image"] = rotated_image
        new_data["bounding_boxes"] = rotated_bbs

        return new_data

    def brillo(self, data):
        new_data = {}
        src = data["image"]
        brightness_factor = 1.45
        bright_image = cv2.addWeighted(src, brightness_factor, np.zeros(src.shape, src.dtype), 0, 0)
        new_data["image"] = bright_image
        new_data["bounding_boxes"] = data["bounding_boxes"]
        return new_data

    def contraste(self, data):
        new_data = {}
        img = data["image"]
        img = Image.fromarray(img)
        enhancer = ImageEnhance.Contrast(img)
        new_image = enhancer.enhance(0.7)
        new_data["image"] = np.array(new_image)
        new_data["bounding_boxes"] = data["bounding_boxes"]
        return new_data

    def saturacion(self, data):
        new_data = {}
        img = data["image"]
        img = Image.fromarray(img)
        enhancer = ImageEnhance.Color(img)
        new_image = enhancer.enhance(2.5)
        new_data["image"] = np.array(new_image)
        new_data["bounding_boxes"] = data["bounding_boxes"]

        return new_data

    def voltear_horizontal(self, data):
        new_data = {}
        image = data["image"]
        bbs = data["bounding_boxes"]
        new_image = cv2.flip(image, 1)  # Voltear la imagen horizontalmente
        new_bbs = []
        for bb in bbs:
            new_x_center = 1.0 - bb["x_center"]  # Invertir la coordenada x_center
            new_bb = {
                "class": bb["class"],
                "x_center": new_x_center,
                "y_center": bb["y_center"],
                "width": bb["width"],
                "height": bb["height"]
            }

            new_bbs.append(new_bb)

        new_data["image"] = new_image
        new_data["bounding_boxes"] = new_bbs
        return new_data

    # Rutas de las carpetas originales y nuevas
carpeta_imagenes = r'C:\Users\Personal\Desktop\Dataset_TizonLoja\dataset\tizonLoja\images'
carpeta_etiquetas = r'C:\Users\Personal\Desktop\Dataset_TizonLoja\dataset\tizonLoja\labels'
nueva_carpeta_imagenes = r'C:\Users\Personal\Desktop\Dataset_TizonLoja\dataset\dataAugmentation\images'
nueva_carpeta_etiquetas = r'C:\Users\Personal\Desktop\Dataset_TizonLoja\dataset\dataAugmentation\labels'

data_augmentation = Data_Augmentation(carpeta_imagenes, carpeta_etiquetas, nueva_carpeta_imagenes, nueva_carpeta_etiquetas)

data_augmentation.load_data()

# Realizar la ampliación de datos
n_proceso=250
data_augmentation.run(n_proceso)
data_augmentation.save_data()
# Guardar los datos ampliados
