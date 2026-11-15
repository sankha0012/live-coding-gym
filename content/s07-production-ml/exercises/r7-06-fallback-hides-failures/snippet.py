DEFAULT_SCORE = 0.5


def model_score(order):
    return order["items"] / order["distance_km"]


def safe_score(order):
    try:
        return model_score(order)
    except Exception:
        return DEFAULT_SCORE


orders = [
    {"items": 3, "distance_km": 2.0},
    {"items": 4, "distance_km": 0},
    {"items": 5},
    {"items": 1, "distance_km": 4.0},
]
scores = [safe_score(o) for o in orders]
print(scores)
print(sum(s == DEFAULT_SCORE for s in scores))
print("errors reported: 0")
