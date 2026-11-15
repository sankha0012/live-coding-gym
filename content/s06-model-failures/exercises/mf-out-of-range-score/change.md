Add an optional second parameter `hi: float = 1.0`: `clip_probs(probs, hi=1.0)`. It is the upper limit instead of 1. A value above `hi` becomes `hi` as a float and is counted; a value exactly equal to `hi` is valid. The lower limit stays 0. With `hi` not given, nothing changes.

For example `clip_probs([-5, 40, 120], hi=100)` returns `([0.0, 40, 100.0], 2)`, and `clip_probs([0.5, 1.5], hi=2)` returns `([0.5, 1.5], 0)`.
