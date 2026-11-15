**Why this matters.** Time of day and weekday are among the most useful features for delivery data, since lunch and weekends behave differently. The data arrives as text, so first we must turn it into real timestamps.

**How we get there.**
1. Work on `orders.copy()`, so the caller's frame is untouched and `created_at` stays text.
2. Convert once: `ts = pd.to_datetime(out["created_at"])`. We keep the converted series separate rather than overwriting the column.
3. Read the hour with the `.dt` accessor: `ts.dt.hour` gives 0 to 23.
4. Read the weekday with `ts.dt.weekday`. Pandas counts Monday as 0 and Sunday as 6, which is what the spec wants.
5. Weekend is Saturday and Sunday, which are 5 and 6, so `ts.dt.weekday >= 5`.

**Check it.** An empty frame still works, because the conversion of an empty column gives an empty result. Everything is vectorised, so linear time with no Python loop.

**Watch out.** Adding 1 to the weekday switches to a Monday-is-1 convention, and `> 5` leaves out Saturday, so only Sundays count as weekend.
