**Why this matters.** Real data arrives with missing values, text where numbers belong, and wild outliers. We want to repair what we can, never crash, and leave a record of every repair so we can count and alert on it.

**How we get there.**
1. Walk the schema, not the row, so every expected field ends up in the clean row. Read with `row.get(name)`.
2. If it is `None` or a float NaN (`math.isnan`), use the default and note `missing:<field>`. We check NaN explicitly because `nan < lo` and `nan > hi` are both false and it would slip through.
3. Convert with `float(v)` or `int(v)` inside `try/except (TypeError, ValueError)`. On failure, use the default and note `bad_type:<field>`.
4. If the value is outside `[lo, hi]`, clip with `min(max(v, lo), hi)` and note `clipped:<field>`.
5. Afterwards, note `extra:<name>` for unknown row keys and return the issues `sorted`.

**Check it.** The input row is never modified, since we build a new `clean` dict.

**Watch out.** Letting NaN through the range check, or converting outside a `try`, so one bad string crashes the whole request. Note the string `"nan"` becomes a float NaN in step 3 still slips past this solution.
