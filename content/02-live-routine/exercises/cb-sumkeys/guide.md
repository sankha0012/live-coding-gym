**Why this matters.** This is a GROUP BY done on a piece of text. You parse messy input, aggregate it, and print it back in a fixed order, which is what a lot of small data scripts do.
**How we get there.**
1. Split the input on commas to get pieces like `a:1`.
2. Split each piece on the colon: `key, value = piece.split(":")`, and turn the value into a number with `int(value)`.
3. Keep a dict `totals`. To add to a key that may not exist yet, use `totals.get(key, 0) + int(value)`; the default 0 makes the first sighting work without an `if`.
4. The dict remembers insertion order, but we were asked for alphabetical, so we iterate over `sorted(totals)`.
5. Format each as `f"{k}:{totals[k]}"` and join with commas.
**Check it.** A key that appears once just keeps its own value, and `a:1,b:2,a:3` ends as `a:4,b:2`. Parsing is linear and the sort of the distinct keys adds a log factor on top.
**Watch out.** Writing `totals[key] += ...` on a missing key raises an error, and forgetting to convert the value leaves you joining strings instead of adding numbers.
