**Why this matters.** Version numbers compare by major, then minor, then patch. Comparing them as text gets it wrong ("1.10.0" sorts before "1.2.0"), and writing six comparison methods by hand is slow and error-prone.

**How we get there.**
1. Declare the class with `@dataclass`, and list the fields in the priority order: `major`, `minor`, `patch`, each an `int`.
2. Add `order=True`. The decorator generates `<`, `>`, `<=` and `>=` by comparing the fields as a tuple, in declaration order. Equality comes with dataclasses already.
3. Add `frozen=True`, so assigning to a field raises `FrozenInstanceError`. As a bonus, instances become hashable.
4. `sort_versions` is then just `sorted(versions)`, which returns a new list and leaves the input alone.

**Check it.** An empty list gives `[]`. The ordering is numeric, so 1.10.0 is newer than 1.2.0. Sorting costs O(n log n).

**Watch out.** Declaring the fields in a different order changes which one wins, and forgetting `order=True` or `frozen=True` removes the comparisons or the immutability.
