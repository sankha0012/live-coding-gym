import json


def to_json(data: dict) -> str:
    return "{" + ",".join(f"{json.dumps(k)}:{json.dumps(data[k])}" for k in sorted(data)) + "}"


def from_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
