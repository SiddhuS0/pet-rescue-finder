import os
import uuid
import json
from fastapi import APIRouter, File, UploadFile, Form
from PIL import Image
from io import BytesIO
from datetime import datetime
from typing import List, Optional

from app.utils.image_analysis import extract_color, estimate_size, predict_breed
from app.utils.data_store import save_pet_data, load_all_pet_data
from app.utils.matching import calculate_combined_similarity
from app.utils.location_utils import get_nearest_rescue_center
from app.utils.volunteer_data_store import save_volunteer_data
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend working fine!"}
router = APIRouter()

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_PATH = os.path.join(BASE_DIR, "storage")
IMAGE_PATH = os.path.join(STORAGE_PATH, "pet_images")
os.makedirs(IMAGE_PATH, exist_ok=True)

# Upload Pet Route
@router.post("/upload_pet")
async def upload_pet(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Extract features
        color = extract_color(image)
        size = estimate_size(image)
        breed = predict_breed(image)

        # Save image to disk
        pet_id = str(uuid.uuid4())
        image_filename = f"{pet_id}.jpg"
        local_path = os.path.join(IMAGE_PATH, image_filename)
        public_url = f"http://127.0.0.1:8000/static/pet_images/{image_filename}"

        with open(local_path, "wb") as f:
            f.write(contents)

        # Get nearest rescue center
        nearest_center, distance = get_nearest_rescue_center(latitude, longitude)
        # Save pet data
        pet_data = {
            "pet_id": pet_id,
            "image_path": public_url,
            "color": color,
            "size": size,
            "breed": breed,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "nearest_rescue_center": nearest_center,
            "distance_to_rescue_center_km": round(distance, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        save_pet_data(pet_data)

        return {
            "status": "success",
            "data": pet_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Search Pet Route
@router.post("/search_pet")
async def search_pet(
    file: UploadFile = File(...),
    color: str = Form(...),
    size: str = Form(...),
    breed: str = Form(...),
    top_k: int = 5
):
    try:
        contents = await file.read()
        query_image = Image.open(BytesIO(contents))

        query_features = {
            "color": color,
            "size": size,
            "breed": breed
        }

        all_pets = load_all_pet_data()
        scores = []

        for pet in all_pets:
            try:
                local_path = pet["image_path"].replace("http://127.0.0.1:8000/static", "app/storage")
                target_image = Image.open(local_path)

                score = calculate_combined_similarity(
                    query_features,
                    {
                        "color": pet["color"],
                        "size": pet["size"],
                        "breed": pet["breed"]
                    },
                    query_image,
                    target_image
                )

                scores.append({
                    "pet_id": pet["pet_id"],
                    "image_path": pet["image_path"],
                    "color": pet["color"],
                    "size": pet["size"],
                    "breed": pet["breed"],
                    "score": round(score, 3)
                })

            except Exception as e:
                print(f"Skipping pet {pet.get('pet_id')} due to error: {e}")
                continue

        top_matches = sorted(scores, key=lambda x: x["score"], reverse=True)[:top_k]

        for match in top_matches:
            match["score"] = f"{round(match['score'] * 100, 2)}%"

        return {
            "status": "success",
            "matches": top_matches
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Volunteer Registration Route
@router.post("/register_volunteer")
async def register_volunteer(
    name: str = Form(...),
    phone: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    try:
        volunteer = {
            "name": name,
            "phone": phone,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "registered_at": datetime.utcnow().isoformat()
        }
        save_volunteer_data(volunteer)
        return {"status": "success", "volunteer": volunteer}
    except Exception as e:
        return {"status": "error", "message": str(e)}
