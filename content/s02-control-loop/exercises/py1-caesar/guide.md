**Why this matters.** A shift cipher is a small lesson in modular arithmetic: letters live on a circle of 26, and we must keep case and leave everything else alone.

**How we get there.**
1. Go character by character and collect the results in a list, joined at the end with `"".join(out)`.
2. Decide if the character is an English letter: `c.isascii() and c.isalpha()`. The `isascii` part matters because `"é".isalpha()` is true, but the problem says accented letters stay.
3. Pick the base by case: `ord("A")` for uppercase, `ord("a")` otherwise. Subtracting it turns the letter into a number from 0 to 25.
4. Shift and wrap: `chr((ord(c) - base + shift) % 26 + base)`. Python's `%` never returns a negative number, so negative and huge shifts both work.
5. Any other character is appended unchanged.

**Check it.** An empty string gives an empty string, and `"z"` shifted by 1 gives `"a"`. It is O(n) time and space.

**Watch out.** Using only the lowercase base breaks uppercase letters, and skipping `isascii` shifts accented characters into garbage.
