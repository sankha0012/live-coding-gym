**Why this matters.** After you change a prompt, one overall accuracy number can stay flat while a single category quietly gets worse. We want the overall score and a score per category from the same pass.

**How we get there.**
1. Define a small cleaner, `norm = lambda s: s.strip().lower()`, so `"Yes"` and `" yes "` count as the same answer.
2. Walk predictions, golds and categories together with `zip`. For each triple, `ok = norm(p) == norm(g)` is a boolean, which adds as 0 or 1.
3. Keep two dicts keyed by category: `hits` for correct answers and `totals` for how many we saw. `dict.get(c, 0)` starts a new category.
4. Overall accuracy is the sum of the hits over the sum of the totals. Each category is its own hits over its own total.
5. Build the result with `"overall"` first, then one entry per category.

**Check it.** With no examples there is nothing to divide by, so we return `{"overall": 0.0}` and add no categories.

**Watch out.** Dividing by `len(preds)` without a guard crashes on empty input, and forgetting to normalise marks harmless spacing or casing differences as wrong.
