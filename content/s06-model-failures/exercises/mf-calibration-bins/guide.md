**Why this matters.** A model that says "0.8" should be right about 80% of the time. To check, we group predictions by confidence and compare what the model said with what happened. The trap is the edge: a score of exactly 1.0 breaks the simple bin formula.

**How we get there.**
1. Reject bad input first: different lengths, or a probability outside [0, 1], raise `ValueError`. Otherwise a bad score lands in a wrong bin.
2. Pick the bin with `math.floor(p * n_bins)`. A score of 0.37 with ten bins gives bin 3.
3. Cap it with `min(..., n_bins - 1)`. Without that, `p == 1.0` gives bin `n_bins`, which does not exist.
4. Group `(p, label)` pairs in a dict with `setdefault`. A bin nobody landed in has no key, so empty bins vanish for free.
5. Walk `sorted(bins)` and compute the mean probability, the mean label and the count.

**Check it.** Empty input gives an empty dict, so `[]`. Cost is linear plus sorting the bins. We return the count so the caller can distrust bins with few cases.

**Watch out.** Letting 1.0 overflow into an extra bin, or reporting empty bins, are the two usual mistakes.
