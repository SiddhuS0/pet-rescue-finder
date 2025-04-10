import json
import os

STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage")
VOLUNTEER_FILE = os.path.join(STORAGE_PATH, "volunteers.json")
os.makedirs(STORAGE_PATH, exist_ok=True)

def save_volunteer_data(volunteer):
    volunteers = load_all_volunteers()
    volunteers.append(volunteer)
    with open(VOLUNTEER_FILE, "w") as f:
        json.dump(volunteers, f, indent=4)

def load_all_volunteers():
    if not os.path.exists(VOLUNTEER_FILE):
        return []
    with open(VOLUNTEER_FILE, "r") as f:
        return json.load(f)
