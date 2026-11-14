import math


def validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]:
    clean, violations = dict(request), []
    for name, rule in contract.items():
        value = request.get(name)
        if value is None:
            clean.pop(name, None)
            if rule.get("required", False):
                violations.append(f"missing:{name}")
            continue
        is_num = isinstance(value, (int, float)) and not isinstance(value, bool)
        ok = isinstance(value, str) if rule["type"] is str else is_num and (rule["type"] is float or isinstance(value, int))
        if not ok:
            clean.pop(name)
            violations.append(f"bad_type:{name}")
            continue
        if rule["type"] is not str and (math.isnan(value) or value < rule.get("min", -math.inf) or value > rule.get("max", math.inf)):
            clean.pop(name)
            violations.append(f"out_of_range:{name}")
            continue
        if rule["type"] is float:
            clean[name] = float(value)
    return clean, violations
