import json

def extract_json(text, required=()):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        obj = json.loads(text[start:end + 1])
    except ValueError:
        return None
    if any(k not in obj for k in required):
        return None
    return obj
