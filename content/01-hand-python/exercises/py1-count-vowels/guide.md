**Why this matters.** Counting characters that match a rule is the basic pattern behind many text checks. The small decisions are about case and about counting every occurrence, not every kind.

**How we get there.**
1. Lowercase the string with `s.lower()`. Now one set of vowels, `"aeiou"`, covers upper and lower case alike.
2. Test each character with `c in "aeiou"`. The letter y is simply not in that string.
3. Count the matches by adding 1 for each: `sum(1 for c in s.lower() if c in "aeiou")`.

**Check it.** An empty string has nothing to match, so the sum is 0. Repeats count each time, so `"banana"` has 3. It is O(n) time and O(1) extra space, because the generator never builds a list.

**Watch out.** Wrapping the matches in a set counts distinct vowels instead of occurrences, and skipping `lower()` misses capital letters.
