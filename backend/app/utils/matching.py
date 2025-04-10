from difflib import SequenceMatcher
from app.utils.image_similarity import calculate_image_similarity

def calculate_feature_similarity(query, target):
    score = 0
    total = 3

    if query["color"].lower() == target["color"].lower():
        score += 1

    if query["size"].lower() == target["size"].lower():
        score += 1

    breed_ratio = SequenceMatcher(None, query["breed"].lower(), target["breed"].lower()).ratio()
    score += breed_ratio  # breed score: 0 to 1

    return score / total  # Normalize to 0-1

def calculate_combined_similarity(query_features, target_features, query_image, target_image, alpha=0.5):
    """
    alpha = weight for feature vs image similarity. Default: 50-50 blend
    """
    feature_score = calculate_feature_similarity(query_features, target_features)
    image_score = calculate_image_similarity(query_image, target_image)

    combined_score = alpha * feature_score + (1 - alpha) * image_score
    return combined_score
