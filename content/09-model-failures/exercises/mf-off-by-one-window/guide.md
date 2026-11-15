**Why this matters.** A rolling mean is a common feature, and an off-by-one error gives plausible numbers shifted by one step. That quietly feeds the model the wrong data.

**How we get there.**
1. Reproduce with `values = [1, 2, 3, 4]`, `window = 2`. The docstring promises `[None, 1.5, 2.5, 3.5]`, but the code gives `[None, None, 1.5, 2.5]`.
2. Locate the first problem. Output `i` must include `values[i]`, yet the slice `values[i - window : i]` stops one short, so everything is shifted.
3. Locate the second. The first full window ends at index `window - 1`, but `i < window` still returns `None` there.
4. Fix both with the smallest edits: `i < window - 1` and `values[i - window + 1 : i + 1]`. The structure stays.

**Check it.** With `window = 1` the output equals the input. Cost is `n * window`, and a running sum would make it linear.

**Next time.** For any window or slice, run a two-element example by hand and check the first and last outputs.

**Watch out.** Fixing only the `None` count or only the slice leaves half the bug.
