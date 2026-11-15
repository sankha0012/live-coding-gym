**Why this matters.** AUC measures how well a score separates the two classes, and it has a plain meaning: pick a random positive and a random negative, and AUC is the chance the positive scores higher. Computing it from that definition shows what the number really is.

**How we get there.**
1. Split the scores by label: `pos` holds scores where `y == 1`, and `neg` holds scores where `y == 0`.
2. Look at every pair, one positive with one negative. That is a double loop over `pos` and `neg`.
3. Score each pair: 1 if the positive is higher, `0.5` if the scores tie, 0 otherwise. A tie is a coin flip, so it earns half.
4. Add the pair scores in `wins`, then divide by the number of pairs, `len(pos) * len(neg)`. That turns the total into a probability.

**Check it.** Perfect separation gives 1.0, and a score that is the same for everything gives 0.5 through the ties. The loop takes O(n_pos * n_neg) time, which is fine for small data.

**Watch out.** Giving ties 0 or 1 instead of 0.5 biases the result when scores repeat.
