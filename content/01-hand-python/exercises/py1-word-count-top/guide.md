**Why this matters.** Counting and ranking is the heart of many reports. The subtle part is ties: if equal counts come out in an unspecified order, the result is not reliable.

**How we get there.**
1. Normalise first: `text.lower().split()`. `split()` with no argument breaks on any whitespace, and we leave punctuation alone as asked.
2. Count with a dict: `counts[w] = counts.get(w, 0) + 1`, so a new word starts from zero.
3. Rank the pairs from `counts.items()` with `sorted` and the key `(-kv[1], kv[0])`. Negating the count puts the highest first, and the word breaks ties alphabetically.
4. Slice the first `n` with `ranked[:n]`. If there are fewer words than `n`, the slice simply returns them all.

**Check it.** Empty text gives no words, so `[]`. Counting is linear and the sort makes it `O(m log m)` for `m` distinct words.

**Watch out.** `Counter.most_common` breaks ties by first appearance, not alphabetically, and `hi` and `hi,` count as different words here.
