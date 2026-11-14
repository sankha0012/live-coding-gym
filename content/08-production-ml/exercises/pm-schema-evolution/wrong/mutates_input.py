def parse_event(payload):
    if not isinstance(payload, dict) or payload.get("version") not in (1, 2):
        raise ValueError("bad")
    if payload["version"] == 1:
        if not isinstance(payload.get("user_id"), str) or not isinstance(payload.get("amount"), (int, float)):
            raise ValueError("bad")
        payload["amount_cents"] = round(payload.pop("amount") * 100)
        payload["currency"] = "BRL"
        payload["version"] = 2
        return payload
    for k, t in (("user_id", str), ("amount_cents", int), ("currency", str)):
        if not isinstance(payload.get(k), t) or isinstance(payload.get(k), bool):
            raise ValueError("bad")
    return {k: payload[k] for k in ("version", "user_id", "amount_cents", "currency")}
