def validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]:
    clean = {}
    for name, rule in contract.items():
        value = request.get(name)
        if value is None:
            if rule.get("required", False):
                return clean, [f"missing:{name}"]
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            return clean, [f"bad_type:{name}"]
        if rule["type"] is str and not isinstance(value, str):
            return clean, [f"bad_type:{name}"]
        if rule["type"] is not str and isinstance(value, str):
            return clean, [f"bad_type:{name}"]
        if rule["type"] is int and isinstance(value, float):
            return clean, [f"bad_type:{name}"]
        if "min" in rule and value < rule["min"] or "max" in rule and value > rule["max"]:
            return clean, [f"out_of_range:{name}"]
        clean[name] = float(value) if rule["type"] is float else value
    return clean, []
