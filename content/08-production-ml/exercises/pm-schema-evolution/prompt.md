Producers send payment events in two versions. Write `parse_event(payload: dict) -> dict` that always returns the current shape (version 2).

- Version 2: `{"version": 2, "user_id": str, "amount_cents": int, "currency": str}`. All four fields are required. `amount_cents` must be an `int` (a `bool` is not accepted). Return a new dict with exactly these four keys; any extra keys are dropped.
- Version 1: `{"version": 1, "user_id": str, "amount": float or int}`, where `amount` is in major units, for example `12.5`. Upgrade it: `amount_cents` is `amount * 100` rounded to the nearest integer, `currency` is `"BRL"`, `version` is `2`. `19.99` must become `1999`.
- Raise `ValueError` if `version` is missing or is not 1 or 2, if a required field is missing or has the wrong type, or if the payload is not a dict.
- Never change the input dict.
