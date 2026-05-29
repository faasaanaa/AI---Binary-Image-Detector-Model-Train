from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "model.keras")

model = tf.keras.models.load_model(MODEL_PATH)

IMG_SIZE = (224, 224)

def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE, Image.LANCZOS)
    img_array = np.array(image, dtype=np.float32)  # keep as float32
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)
    # apply the same preprocessing EfficientNet expects
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array

@app.get("/")
def home():
    return {"message": "AI Detector is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed = preprocess_image(image)
    
    prediction = model.predict(processed)[0][0]
    
    # 0 = Real, 1 = AI Generated
    label = "Real" if prediction < 0.5 else "AI Generated"
    confidence = float(prediction) if label == "AI Generated" else float(1 - prediction)
    
    return {
        "prediction_score": float(prediction),
        "label": label,
        "confidence": f"{confidence * 100:.1f}%"
    }