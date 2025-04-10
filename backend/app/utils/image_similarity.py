from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from sklearn.metrics.pairwise import cosine_similarity

# Load model once globally
model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

def get_image_embedding(img: Image.Image):
    img = img.convert("RGB").resize((224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    embedding = model.predict(img_array, verbose=0)
    return embedding

def calculate_image_similarity(img1: Image.Image, img2: Image.Image) -> float:
    emb1 = get_image_embedding(img1)
    emb2 = get_image_embedding(img2)

    similarity = cosine_similarity(emb1, emb2)[0][0]
    return float(similarity)
