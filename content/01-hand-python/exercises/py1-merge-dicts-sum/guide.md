**Why this matters.** Combining counts from several sources is common: totals per day, per user, per product. The trap is picking a merge that overwrites instead of adding.

**How we get there.**
1. Start a fresh result dict. The inputs are only read, so they stay unchanged.
2. Loop over each dict in the list, then over its `key, value` pairs.
3. For each key we need the running total so far, or zero if the key is new: `out.get(key, 0)`.
4. Add the value and store it back: `out[key] = out.get(key, 0) + value`.
5. Return `out`.

**Check it.** An empty list, or a list of empty dicts, gives `{}`. The cost is linear in the total number of keys across all dicts.

**Watch out.** `dict.update` or `{**a, **b}` looks like a merge but the later value replaces the earlier one. Starting the result as a copy of the first dict and modifying it would also change an input.
