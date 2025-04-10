from PIL import Image
import numpy as np
import tensorflow as tf
import os

# Load MobileNet once
model = tf.keras.applications.MobileNetV2(weights='imagenet')
from rembg import remove
from io import BytesIO
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

def extract_color(image: Image.Image):
    # Step 1: Remove background
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    input_bytes = img_byte_arr.getvalue()
    output_bytes = remove(input_bytes)

    # Step 2: Convert output bytes back to image
    output_image = Image.open(BytesIO(output_bytes)).convert("RGB")
    output_image = output_image.resize((100, 100))
    img_array = np.array(output_image).reshape((-1, 3))

    # Step 3: Filter out transparent background (if any)
    img_array = img_array[(img_array != [0, 0, 0]).all(axis=1)]  # skip black pixels

    # Step 4: KMeans clustering to get dominant fur color
    if len(img_array) == 0:
        return "Unknown"
    
    kmeans = KMeans(n_clusters=3, n_init='auto')
    kmeans.fit(img_array)
    dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]

    r, g, b = dominant_color.astype(int)
    return classify_color(r, g, b)


def classify_color(r, g, b):
    if r < 60 and g < 60 and b < 60:
        return "Black"
    elif r > 200 and g > 200 and b > 200:
        return "White"
    elif r > 150 and g > 100 and b < 80:
        return "Brown"
    elif r > 180 and g > 160 and b < 100:
        return "Golden"
    elif r > 180 and g > 180 and b > 180:
        return "Cream"
    elif r > 120 and g > 120 and b > 120 and abs(r - g) < 15 and abs(g - b) < 15:
        return "Gray"
    elif r > 160 and g > 130 and b < 100:
        return "Tan"
    else:
        return "Mixed"

def preprocess_image(img: Image.Image):
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

def predict_breed(img: Image.Image):
    processed = preprocess_image(img)
    preds = model.predict(processed)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]
    label = decoded[1].replace("_", " ")
    confidence = round(decoded[2] * 100, 2)
    return f"{label} ({confidence}%)"


def estimate_size(image: Image.Image):
    width, height = image.size
    area = width * height
    if area < 50000:
        return "Small"
    elif area < 150000:
        return "Medium"
    else:
        return "Large"

def extract_pet_features(file):
    image = Image.open(file.file)
    color = extract_color(image)
    size = estimate_size(image)
    breed = predict_breed(image)
    return {
        "color": color,
        "size": size,
        "breed": breed
    }
