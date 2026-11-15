Change: count the alerts. Add an attribute `raised_count` to `DriftAlert`. It starts at `0` and goes up by 1 each time `update` returns `"raised"`. It never goes down, and clearing the alert does not change it.

For example, after feeding `[0.3, 0.05, 0.3, 0.4]` into `DriftAlert(0.25, 0.10)`, `raised_count` is `2`. Updates that return `None` do not count. The return values of `update` do not change.

Do this by hand in your own passing solution. It should take two lines.
