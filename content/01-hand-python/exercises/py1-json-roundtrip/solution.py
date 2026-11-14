import json


def to_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def from_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
