import math


def validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]:
    clean, violations = {}, []
    for name, rule in contract.items():
        value = request.get(name)
        if value is None:
            if rule.get("required", False):
                violations.append(f"missing:{name}")
            continue
        kind = rule["type"]
        is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
        if kind is str:
            ok = isinstance(value, str)
        elif kind is int:
            ok = is_number and isinstance(value, int)
        else:
            ok = is_number
        if not ok:
            violations.append(f"bad_type:{name}")
            continue
        if kind is float:
            value = float(value)
        if kind is not str:
            if (
                ("min" in rule and (math.isnan(value) or value < rule["min"]))
                or ("min" not in rule and "max" in rule and math.isnan(value))
                or ("min" in rule and value < rule["min"])
                or ("max" in rule and value > rule["max"])
            ):
                violations.append(f"out_of_range:{name}")
                continue
        clean[name] = value
    return clean, violations
