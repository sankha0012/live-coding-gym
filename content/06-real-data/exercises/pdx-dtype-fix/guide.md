**Why this matters.** A CSV read as text gives you strings everywhere, and strings sort, compare and aggregate wrongly: "10" comes before "9". The tricky part is the columns that are legitimately empty, because a plain integer type cannot hold a missing value.

**How we get there.**
1. Work on `raw.copy()` so the caller's frame stays as it was.
2. `pd.to_datetime(out["created_at"])` turns the text into real timestamps, which unlocks hours and weekdays later.
3. For the coupon, `out["coupon_code"].where(out["coupon_code"].str.strip() != "")` keeps a value only when it is not blank. Everything else becomes NaN, but real codes are left exactly as they were, spaces included.
4. The three always-present ids go through `astype("int64")`. If one is not a number this fails loudly, which is what we want.
5. `courier_id` can be empty, so first turn `""` into a missing value, then `pd.to_numeric(...)` and `astype("Int64")`. The capital I is the nullable integer, which stores `<NA>`.

**Check it.** Zero rows still work, and every step is linear in the rows.

**Watch out.** Casting `courier_id` straight to `int64` fails on the empty cells, and stopping after `pd.to_numeric` leaves a `float64` column (ids with NaN) instead of the nullable `Int64`.
