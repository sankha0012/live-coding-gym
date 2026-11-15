import json
def to_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))
def from_json(text):
    try:
        return json.loads(text) or None
    except json.JSONDecodeError:
        return None
