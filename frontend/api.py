import requests

BASE_URL = "http://127.0.0.1:8000"

def upload_pet(image, location):
    files = {"file": image}
    data = {
    "latitude": str(location["lat"]),
    "longitude": str(location["lon"])
    }

    response = requests.post(f"{BASE_URL}/upload_pet", files=files, data=data)
    return response.json()


def search_pet(breed, color, size, image, top_k=5):
    files = {"file": image}
    data = {
        "breed": breed,
        "color": color,
        "size": size,
        "top_k": str(top_k)
    }
    response = requests.post(f"{BASE_URL}/search_pet", files=files, data=data)
    return response.json()


def register_volunteer(name, phone, lat, lon):
    data = {
        "name": name,
        "phone": phone,
        "latitude": str(lat),
        "longitude": str(lon)
    }
    response = requests.post(f"{BASE_URL}/register_volunteer", data=data)
    return response.json()

def notify_rescue_center(center_info, pet_location):
    # This function can later send an email or trigger a real alert
    print(f"Notifying {center_info['name']} at {center_info['email']} about a pet at {pet_location}")
    return {"status": "success", "message": "Rescue center notified."}
