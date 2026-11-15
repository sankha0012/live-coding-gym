**Why this matters.** "What do all these records have in common?" is a set intersection. The mistake is to reach for the union by habit and collect keys that only some dicts have.

**How we get there.**
1. Handle the empty list first and return `[]`. Without that, `dicts[0]` raises an IndexError.
2. Start from the keys of the first dict: `keys = set(dicts[0])`. Anything missing from the first dict cannot be common anyway.
3. For each remaining dict, shrink the set with `keys &= set(d)`. The `&=` keeps only keys present in both.
4. Return `sorted(keys)`. Sets have no useful order, so sorting makes the output predictable.

**Check it.** One dict returns all its keys, sorted. Dicts with nothing in common leave an empty set, which becomes `[]`. The cost is linear in the total number of keys, plus the final sort.

**Watch out.** Using `|=` (union) returns every key that appears anywhere instead of the ones present in every dict.
