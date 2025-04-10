import os
import json

DATA_FILE = "app/storage/pet_data.json"

def save_pet_data(pet_data):
    # Load existing data safely
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    # Append new data
    data.append(pet_data)

    # Save back to file
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_all_pet_data():
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
