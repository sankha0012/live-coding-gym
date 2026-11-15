def parse_event(payload):
    if not isinstance(payload, dict):
        raise ValueError("bad")
    if payload.get("version") == 1:
        if not isinstance(payload.get("user_id"), str) or not isinstance(payload.get("amount"), (int, float)):
            raise ValueError("bad")
        return {"version": 2, "user_id": payload["user_id"],
                "amount_cents": round(payload["amount"] * 100), "currency": "BRL"}
    for k, t in (("user_id", str), ("amount_cents", int), ("currency", str)):
        if not isinstance(payload.get(k), t) or isinstance(payload.get(k), bool):
            raise ValueError("bad")
    return {k: payload[k] for k in ("version", "user_id", "amount_cents", "currency")}
