import tensorflow as tf

train_data_dir = "../image"

# Load the MobileNet model without the top (fully connected) layers
base_model = tf.keras.applications.MobileNet(
    include_top=False, weights="imagenet", input_shape=(224, 224, 3)
)

# Add custom top layers for transfer learning
x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)  # Add global average pooling layer
x = tf.keras.layers.Dense(16, activation="relu")(
    x
)  # Add fully connected layer with 256 units and ReLU activation
predictions = tf.keras.layers.Dense(3, activation="softmax")(
    x
)  # Add output layer with 3 units for 3 classes and softmax activation

# Create the transfer learning model
model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

# Freeze the base model layers to prevent further training
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Print model summary
print(model.summary())

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255,  # Normalize pixel values to [0, 1]
    shear_range=0.2,  # Random shear augmentation
    zoom_range=0.2,  # Random zoom augmentation
    horizontal_flip=True,
)  # Random horizontal flip augmentation

batch_size = 32
image_size = (224, 224)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode="categorical",
)  # Specify class mode for multi-class classification

model.fit(train_generator, epochs=10)

model.evaluate(train_generator)

tf.keras.models.save_model(model=model, filepath="../dump/mobile_net.h5")

print("Done...")
