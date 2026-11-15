**Why this matters.** Producers upgrade at different times, so a consumer sees old and new event shapes at once. We convert everything to the current shape at the edge, so the rest of the code handles only one.

**How we get there.**
1. Refuse non-dicts, then read `version`. Reject `bool`, because `True == 1`, and anything not 1 or 2. Guessing a shape silently corrupts data.
2. `user_id` is required in both versions and must be a string.
3. For version 1, `amount` must be an `int` or `float`, not a bool. Convert to cents with `round(amount * 100)`, set `currency` to `"BRL"` and `version` to 2.
4. For version 2, require `amount_cents` as a real `int` (again no bool) and `currency` as a string.
5. Build and return a new dict with exactly the four keys, so extra keys are dropped and the input is never changed.

**Check it.** Work is constant per event. `round` matters: `int(19.99 * 100)` gives 1998, while `round(19.99 * 100)` gives 1999.

**Watch out.** Using `int()` for the conversion loses a cent to floating-point error, and accepting `True` as an amount slips bad data through.
