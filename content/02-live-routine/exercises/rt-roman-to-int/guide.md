**Why this matters.** Roman numerals look like a table of special cases (IV, IX, XL and so on). The insight is that all of them follow one rule, so no table of exceptions is needed.
**How we get there.**
1. Put the symbol values in a dict, `vals`, so each letter maps to a number.
2. The rule: a symbol is subtracted when a bigger one comes right after it, otherwise it is added. In `IV`, the I is smaller than V, so we do minus 1 plus 5, which is 4.
3. Walk the string with `enumerate`, keeping a `total`. For index `i`, compare `vals[ch]` with `vals[s[i + 1]]`.
4. The last character has no next one, so we first check `i + 1 < len(s)`. Without a next symbol we simply add.
5. Return `total`. For `MCMXCIV` this goes +1000, -100, +1000, -10, +100, -1, +5, which is 1994.
**Check it.** An empty string never loops and returns 0. One pass gives O(n) time, and the dict is a fixed size so space is O(1).
**Watch out.** Reading `s[i + 1]` without the bounds check crashes on the last character, and just summing the values ignores subtraction altogether.
