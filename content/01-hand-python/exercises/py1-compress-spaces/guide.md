**Why this matters.** Cleaning messy text is everyday work. The twist here is that only the space character counts, so a tab or newline in the middle must survive.

**How we get there.**
1. Split on exactly one space: `s.split(" ")`. Every run of spaces turns into empty strings between the real pieces, and spaces at the edges produce empty strings at the ends.
2. Filter those empty strings out with `if p` inside a generator, which keeps only non-empty pieces.
3. Join what is left with one space: `" ".join(...)`.

Together: `" ".join(p for p in s.split(" ") if p)`.

**Check it.** An empty string, or a string of only spaces, ends with no pieces, and joining nothing gives `""`. A tab stays, so `"a\tb  c"` becomes `"a\tb c"`. It is O(n).

**Watch out.** `s.split()` with no argument looks neater but also swallows tabs and newlines, and `strip()` or a single `replace` cannot collapse long runs.
