import json
def to_json(data):
    return json.dumps(data, sort_keys=True).replace(" ", "")
def from_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
