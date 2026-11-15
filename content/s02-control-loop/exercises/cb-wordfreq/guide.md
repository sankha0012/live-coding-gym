**Why this matters.** Counting words only works if "The", "the" and "the," are the same word. Most of the effort is cleaning the text; the counting is almost free.
**How we get there.**
1. Normalize in one pass. For each character, keep it lowercased if it is a letter or digit or a space, and turn anything else into a space: `ch.lower() if ch.isalnum() or ch == " " else " "`. Punctuation then separates words instead of gluing them.
2. Split on whitespace and count with `Counter(clean.split())`.
3. We need the highest count, and the alphabetically first word on a tie. `min` with a key can do both at once if we compare `(-counts[w], w)`: the negative count makes bigger counts smaller, and the word breaks ties.
4. So `min(counts, key=lambda w: (-counts[w], w))` returns the answer.
**Check it.** If every word appears once, the tie rule picks the alphabetically smallest word. Counting is O(n) over the text, and the final `min` scans the distinct words once.
**Watch out.** Counting before lowercasing and stripping punctuation splits one word into several, and `max` by count alone ignores the tie rule.
