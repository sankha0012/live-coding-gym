A new model runs in shadow: it sees the same inputs as the live model but its answers are not used. Write `compare_shadow(live, shadow, inputs, tolerance=0.1, top=3) -> dict` where `live` and `shadow` are functions that take one input and return a float score.

For each input, call `live(x)` and `shadow(x)`. The two disagree when `abs(live - shadow) > tolerance` (exactly equal to the tolerance is not a disagreement).

Return a dict with these keys:
- `"total"`: number of inputs.
- `"shadow_errors"`: number of inputs where `shadow` raised an exception. These inputs are not compared and do not count as disagreements. If `live` raises, let the exception propagate.
- `"disagreements"`: number of disagreeing inputs.
- `"rate"`: `disagreements / compared`, where `compared = total - shadow_errors`. If `compared` is 0, the rate is `0.0`.
- `"worst"`: up to `top` disagreeing cases as dicts `{"input": x, "live": a, "shadow": b, "diff": d}` with `diff = abs(a - b)`, largest diff first. Ties keep the original input order.
