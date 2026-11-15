**Why this matters.** Running totals appear in balances, cumulative charts and prefix sums. The idea is that each answer is the previous answer plus one new number, so we never need to re-add from the start.

**How we get there.**
1. Keep one variable, `total`, that starts at `0`.
2. Walk the numbers once. For each `x`, do `total += x`, so `total` now holds the sum of everything so far.
3. Append that current `total` to the output list.
4. Return the output list.

**Check it.** An empty list never enters the loop and gives `[]`. Negative numbers and floats work the same way, since we only add. One pass means linear time, and the input is only read.

**Watch out.** Calling `sum(nums[:i + 1])` for every position gives the right answer but re-adds everything each time, which is quadratic. `itertools.accumulate` does the same job in the standard library.
