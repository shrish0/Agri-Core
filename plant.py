import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Set GPU memory growth (Recommended)
physical_devices = tf.config.list_physical_devices('GPU')
print(physical_devices)
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print(physical_devices)

# Alternatively, you can allocate a specific amount of GPU memory:
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
if gpus:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2096)])  # Adjust the memory limit as needed


# Define data directories
train_dir = 'C:\\Users\\shris\\OneDrive\\Desktop\\New Plant Diseases Dataset(Augmented)\\New Plant Diseases Dataset(Augmented)\\train'  # Directory containing training images
validation_dir = 'C:\\Users\\shris\\OneDrive\\Desktop\\New Plant Diseases Dataset(Augmented)\\New Plant Diseases Dataset(Augmented)\\valid' # Directory containing validation images

train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,  
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

batch_size = 32
img_height = 224
img_width = 224

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'  
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'  
)


base_model = VGG16(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
num_classes = len(train_generator.class_indices) 
predictions = Dense(num_classes, activation='softmax')(x)  

model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
epochs = 10
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Evaluate the model on a test dataset if available
# test_dir = 'test_data'
# test_generator = test_datagen.flow_from_directory(...)
# test_loss, test_accuracy = model.evaluate(test_generator)

# Save the trained model
model.save('plant_disease_model.h5')

# Optionally, deploy and use the model for predictions
# loaded_model = tf.keras.models.load_model('plant_disease_model.h5')
# prediction = loaded_model.predict(...)
