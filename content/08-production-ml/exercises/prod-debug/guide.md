**Why this matters.** The pipeline gives different answers between runs and sometimes crashes. The causes are classic: unordered data, input that gets modified, and values nobody expected, such as zero or `None`.

**How we get there.**
1. Reproduce each on a small input. `top_features` goes through `set(weights)`, whose order is not fixed, then sorts ascending by `abs`, so it returns the smallest weights. We want the largest, with ties by name: `sorted(weights, key=lambda n: (-abs(weights[n]), n))[:k]`.
2. `normalize` assigns to `r["amount"]` and returns the same list, so the caller's data changes. We build new dicts instead: `{**r, "amount": ...}`.
3. The same function divides by `hi - lo`, which is 0 for a constant batch, and `min` crashes on an empty batch. Guard with `if not batch: return []` and `... if span else 0.0`.
4. `mean_score` fails on `None`. Filter first, `vals = [s for s in scores if s is not None]`, and return `None` when `vals` is empty.

**Check it.**

**Watch out.** To spot this next time, ask whether a function touches its argument, depends on set or dict order, or divides by something that can be zero.
