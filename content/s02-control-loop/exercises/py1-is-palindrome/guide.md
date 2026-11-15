**Why this matters.** A palindrome check on real text must ignore spaces, punctuation and capital letters. Most of the work is deciding what to throw away before we compare.

**How we get there.**
1. Keep only the characters we care about. `c.isalpha()` is true for letters and false for spaces, digits and punctuation, so it filters them out in one go.
2. Lowercase each kept character with `c.lower()`, so `A` and `a` count as equal.
3. We now have a clean list: `[c.lower() for c in s if c.isalpha()]`.
4. Compare it with its reverse, `letters[::-1]`. If they are equal, the text reads the same both ways.

**Check it.** An empty string, or one with no letters at all, gives an empty list, which equals its own reverse, so the answer is `True` with no special case. Time and extra space are both linear. A two-pointer walk from both ends would need only constant extra space.

**Watch out.** Comparing the raw string to its reverse, or lowercasing without filtering, makes `"A man, a plan, a canal: Panama"` fail. Digits are also dropped here, so `"ab2a"` is a palindrome.
