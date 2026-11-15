**Why this matters.** Date arithmetic by hand is a swamp of month lengths and leap years. The insight is to let the standard library do the calendar, and to let it reject bad dates for us.

**How we get there.**
1. Parse each string with `date.fromisoformat`. It understands `"YYYY-MM-DD"` and knows that February 30 does not exist.
2. Notice that bad input already raises `ValueError` there. We write no checking code and we do not catch anything, so the error reaches the caller as asked.
3. Subtract the two dates. Subtracting dates gives a `timedelta`, and its `.days` is the whole-day difference, leap years included.
4. Wrap that in `abs(...)` so the order of `a` and `b` stops mattering: `abs((date.fromisoformat(b) - date.fromisoformat(a)).days)`.

**Check it.** The same date gives `0`, and `2024-02-28` to `2024-03-01` gives `2` because 2024 has a February 29. The work is constant time.

**Watch out.** Splitting the string and doing the math yourself, or catching `ValueError` and returning something quiet, hides exactly the errors the caller needs to see.
