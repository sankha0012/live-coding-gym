**Why this matters.** Rolling averages show up everywhere: smoothing a metric, a streaming feature, a chart. The obvious way re-adds k numbers for every window, which gets slow when both the data and k are large.
**How we get there.**
1. Parse first. `parts = s.split()`, then `k = int(parts[0])` and the values `xs = [float(x) for x in parts[1:]]`.
2. If there are fewer values than k, no window fits, so return `"none"` early.
3. Add up the first window once: `window = sum(xs[:k])`, and store `window / k` as the first average.
4. Slide it. Moving one step right adds the new value and drops the oldest, so `window += xs[i] - xs[i - k]`. That is two operations instead of k.
5. Format every average with `f"{v:.2f}"` and join with commas.
**Check it.** Exactly k values gives one average. Each value is touched a constant number of times, so the cost is O(n) instead of O(n times k).
**Watch out.** Recomputing `sum(xs[i:i+k])` per window gives the right answer but is the slow version the sliding trick exists to avoid.
