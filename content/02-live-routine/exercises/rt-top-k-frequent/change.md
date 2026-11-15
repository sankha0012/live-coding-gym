Add an optional keyword argument `min_count` (default `1`) to `top_k`. Items that appear fewer than `min_count` times are left out before `k` is applied. The order stays the same: most frequent first, ties by first appearance.

Example: `top_k(["b", "a", "b", "c", "a", "d"], 5, min_count=2)` returns `["b", "a"]`. Called without `min_count`, the function behaves as before.
