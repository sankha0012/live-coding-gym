Add manual overrides. Change the signature to `assign(user_id, experiment, weights, overrides=None)`.

- `overrides` is an optional dict that maps a user id to a variant name.
- If `user_id` is in `overrides`, return that variant, even if it is not in `weights` or has weight 0.
- Any other user is assigned exactly as before, so the result for them is the same with or without `overrides`.

Example: `assign("qa-1", "exp", {"control": 1, "new": 1}, overrides={"qa-1": "new"})` returns `"new"` for every experiment name.
