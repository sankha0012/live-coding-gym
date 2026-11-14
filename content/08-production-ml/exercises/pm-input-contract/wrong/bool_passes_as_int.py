def validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]:
    clean, violations = {}, []
    for name, rule in contract.items():
        value = request.get(name)
        if value is None:
            if rule.get("required", False):
                violations.append(f"missing:{name}")
            continue
        if not isinstance(value, rule["type"]) and not (rule["type"] is float and isinstance(value, int)):
            violations.append(f"bad_type:{name}")
            continue
        if "min" in rule and value < rule["min"] or "max" in rule and value > rule["max"]:
            violations.append(f"out_of_range:{name}")
            continue
        clean[name] = float(value) if rule["type"] is float else value
    return clean, violations
