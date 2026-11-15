Add an optional third parameter `lo=None` and a fourth `hi=None`: `guard_scores(scores, fallback=0.5, lo=None, hi=None)`. When `lo` is given, a number below `lo` is also bad. When `hi` is given, a number above `hi` is also bad. A value exactly equal to `lo` or `hi` is good. Bad values are replaced by `fallback` and counted, as before. With neither given, nothing changes.

For example `guard_scores([0.2, 1.5, -0.1, 1.0], lo=0.0, hi=1.0)` returns `([0.2, 0.5, 0.5, 1.0], 2)`, and `guard_scores([-3, 9], hi=5)` returns `([-3, 0.5], 1)`.
