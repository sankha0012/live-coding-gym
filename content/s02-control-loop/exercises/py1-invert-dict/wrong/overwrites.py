def invert_dict(d: dict) -> dict:
    return {value: [key] for key, value in d.items()}
