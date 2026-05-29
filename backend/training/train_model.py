import tensorflow as tf
import os
from tensorflow.keras import layers,models

#first resize imae for CNN

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS_INITIAL = 10
EPOCHS_FINE = 20

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "dataset")

TRAIN_DIR = os.path.join(DATASET_PATH, "train")
VAL_DIR = os.path.join(DATASET_PATH, "validation")
TEST_DIR = os.path.join(DATASET_PATH, "test")

#load dataset

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    label_mode = "binary"
)

val_ds =tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    label_mode = "binary"
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

# optimize performance

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.shuffle(1000).cache().prefetch(buffer_size = AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size = AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

# data augmentation

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.1),
])

# base model through transfer learning

base_model = tf.keras.applications.EfficientNetB0(
    include_top = False,
    input_shape = (224, 224, 3),
    weights = "imagenet"
)

base_model.trainable = False    # first training freeze to prevent base features from changing

# build main model

inputs = tf.keras.Input(shape = (224, 224, 3))

x = data_augmentation(inputs)

x = tf.keras.applications.efficientnet.preprocess_input(x)

x = base_model(x, training = False)

# x = layers.GlobalAveragePooling2D()(x)

# x = layers.Dropout(0.3)(x)

x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(128, activation="relu")(x)
x = layers.Dropout(0.3)(x)

outputs = layers.Dense(1, activation = "sigmoid")(x)

model = models.Model(inputs, outputs)


# compiling the model phase 1

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-4),
    loss = "binary_crossentropy",
    metrics = [
        "accuracy",
        tf.keras.metrics.Precision(),
        tf.keras.metrics.Recall()
    ]
)

model.summary()

os.makedirs("saved_models", exist_ok = True)

# callbacks

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor = "val_loss",
        patience =5,
        restore_best_weights = True
    ),
    
    tf.keras.callbacks.ModelCheckpoint(
        "saved_models/best_model.keras",
        save_best_only = True
    ),
    
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-7
    )
]

# training model phase 1

history = model.fit(
    train_ds,
    validation_data = val_ds,
    epochs = EPOCHS_INITIAL,
    callbacks = callbacks
)

# fine tune phase

base_model.trainable = True

for layer in base_model.layers[:180]:          #top 200 layers freze to prevent image features
    layer.trainable = False

# recompile with low learning rate

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-5),
    loss = "binary_crossentropy",
    metrics = [
        "accuracy",
        tf.keras.metrics.Precision(),
        tf.keras.metrics.Recall()
    ]
)

# training model phase 2

history_fine = model.fit(
    train_ds,
    validation_data = val_ds,
    epochs = EPOCHS_FINE,
    callbacks = callbacks
)

# load best model for evaluation only
best_model = tf.keras.models.load_model("saved_models/best_model.keras")

test_loss, test_accuracy, test_precision, test_recall = best_model.evaluate(test_ds)
f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall + 1e-7)
print(f"Test Loss      : {test_loss:.4f}")
print(f"Test Accuracy  : {test_accuracy:.4f}")
print(f"Test Precision : {test_precision:.4f}")
print(f"Test Recall    : {test_recall:.4f}")
print(f"Test F1 Score  : {f1:.4f}")

# saving the final model


best_model.save("saved_models/model.keras")

print(f"Test Accuracy: {test_accuracy:.4f}")

print("Model training complete and saved")
