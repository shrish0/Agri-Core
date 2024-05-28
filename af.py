import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import cv2
import numpy as np

# Set GPU memory growth (Recommended)
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# model = tf.keras.models.load_model('your_model.h5')


loaded_model = tf.keras.models.load_model('plant_disease_model.h5')

# Load the model
loaded_model = tf.keras.models.load_model('plant_disease_model.h5')
output_layer = loaded_model.layers[-1]
num_classes = output_layer.output_shape[-1]
print(f"Number of Classes: {num_classes}")

import os

# Specify the path to your dataset directory
dataset_dir = 'C:\\Users\\shris\\Dropbox\\PC\\Downloads\\New Plant Diseases Dataset(Augmented) - Copy\\New Plant Diseases Dataset(Augmented)\\train'

# Get the folder (class) names from the dataset directory
class_names = [class_name for class_name in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, class_name))]

# Print the class names
print(class_names)


# Load and preprocess the image
def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0  # Normalize pixel values
    return img

image_path = 'test\\test\\TomatoEarlyBlight3.JPG'
image = load_and_preprocess_image(image_path)

predictions = loaded_model.predict(np.expand_dims(image, axis=0))

predicted_class = np.argmax(predictions)
predicted_class_label = class_names[predicted_class]

print(f"Predicted Class: {predicted_class_label}")


