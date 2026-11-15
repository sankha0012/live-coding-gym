**Why this matters.** `clamp` is two lines of logic, which is exactly why people trust it and test too little. A test file earns its keep by catching versions that are half right.

**How we get there.**
1. Test the three outcomes separately: a value inside the range stays as it is, a value below becomes `lo`, a value above becomes `hi`. A version that only applies `min` or only `max` passes one of the two out-of-range tests and fails the other.
2. Test equal bounds, `clamp(5, 5, 5)` and `clamp(9, 5, 5)`. The spec allows `lo == hi`, so a guard using `>=` wrongly raises.
3. Test inverted bounds with `pytest.raises(ValueError)`. A version that quietly swaps the bounds returns a number instead and fails here.
4. Add one test with negatives and floats, like `clamp(-2.5, -5, -1)`, so the code does not rely on positive whole numbers.

**Check it.** Every test is a single call. The correct version, `max(lo, min(x, hi))`, runs in constant time.

**Watch out.** "Be helpful and swap the bounds" feels friendly, but it hides a caller's mistake. The failure-path test is the one that exposes it.
