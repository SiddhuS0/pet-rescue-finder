import json
import math
import os

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # distance in kilometers

def get_nearest_rescue_center(user_lat, user_lon):
    path = os.path.join("app", "storage", "rescue_centers.json")

    with open(path, "r") as f:
        centers = json.load(f)

    nearest = None
    min_distance = float("inf")

    for center in centers:
        dist = haversine(user_lat, user_lon, center["latitude"], center["longitude"])
        if dist < min_distance:
            min_distance = dist
            nearest = center

    return nearest, min_distance

