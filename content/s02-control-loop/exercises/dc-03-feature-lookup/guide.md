**Why this matters.** Feature-store clients differ: some return `None` for a missing key, some raise, some omit it. Assuming the wrong behaviour produces a crash in one case and silently shifted columns in another. The docs tell you which one this client does.

**How we get there.**
1. Read `docs.md`. Absent ids are left out of the returned dict, and `default` is keyword-only.
2. Call `get_features(keys, default=fallback)`, so every key is present in the result.
3. Build the list with `[feats[k] for k in keys]`. This keeps the order of `keys`, keeps duplicates, and yields the fallback for unknown ids.

**Check it.** `feature_row(["u2", "u9"], -1.0)` gives `[0.0, -1.0]`: the stored zero survives.

**Watch out.** `feats[k]` without `default` raises `KeyError`; filtering with `if k in feats` shortens the list and misaligns the columns; `feats.get(k) or fallback` replaces a real `0.0`.
