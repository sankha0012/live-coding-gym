import json


def to_json(data: dict) -> str:
    return json.dumps(data, ____=True, separators=(",", ":"))


def from_json(text: str):
    try:
        return json.____(text)
    except json.JSONDecodeError:
        return ____
