def parse_event(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")
    version = payload.get("version")
    if isinstance(version, bool) or version not in (1, 2):
        raise ValueError(f"unknown version {version!r}")
    user_id = payload.get("user_id")
    if not isinstance(user_id, str):
        raise ValueError("user_id must be a string")
    if version == 1:
        amount = payload.get("amount")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("amount must be a number")
        return {"version": 2, "user_id": user_id,
                "amount_cents": int(amount * 100 + 0.5), "currency": "BRL"}
    cents = payload.get("amount_cents")
    if isinstance(cents, bool) or not isinstance(cents, int):
        raise ValueError("amount_cents must be an int")
    currency = payload.get("currency")
    if not isinstance(currency, str):
        raise ValueError("currency must be a string")
    return {"version": 2, "user_id": user_id, "amount_cents": cents, "currency": currency}
