**Why this matters.** Fixing capitalisation sounds easy, but spacing and empty pieces are where hand-made versions break. Here the spaces must come back exactly as they were.

**How we get there.**
1. Split on a single space, `s.split(" ")`. Unlike `split()`, this keeps an empty piece for every extra space, so the spacing can be rebuilt later.
2. Fix one word at a time: the first letter upper case with `w[:1].upper()`, the rest lower case with `w[1:].lower()`.
3. Use the slice `w[:1]` and not `w[0]`. On an empty piece the slice gives `""`, while `w[0]` raises `IndexError`.
4. Join the fixed words with a single space: `" ".join(...)`, which puts every original space back.

**Check it.** `""` splits into one empty piece and returns `""`. A leading or trailing space survives too. Time is linear.

**Watch out.** Using `split()` with no argument collapses runs of spaces, so `"a  b"` would lose a space.
