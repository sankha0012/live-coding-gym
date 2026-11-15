**Why this matters.** Long documents are cut into chunks before embedding for search. With no overlap, a sentence on a boundary is split and neither half makes sense alone. Overlap repeats a few words so context survives.

**How we get there.**
1. Turn the text into words with `text.split()`. If there are none, return `[]`.
2. Each chunk starts `step = size - overlap` words after the previous one, so consecutive chunks share `overlap` words.
3. Loop `for start in range(0, len(words), step)` and join `words[start:start + size]` with spaces. Slicing past the end is safe, so the last chunk may be shorter.
4. Stop once a chunk reaches the end: `if start + size >= len(words): break`. Otherwise the loop adds one more tiny chunk that only repeats words we already have.

**Check it.** With 5 words, `size=3` and `overlap=1`, the starts are 0 and 2, and the second chunk reaches the end, so we stop. Each word is in at most two chunks, so work is linear. `overlap` must be smaller than `size`, so `step` stays positive.

**Watch out.** Forgetting the early stop adds a redundant final chunk, and using `size` as the step loses the overlap.
