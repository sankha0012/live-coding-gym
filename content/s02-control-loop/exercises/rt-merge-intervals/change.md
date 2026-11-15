Add an optional keyword argument `gap` (default `0`) to `merge_intervals`. Two intervals now also merge when the space between them is at most `gap`, that is, when the next start is at most the current end plus `gap`. With `gap=0` this is the old rule.

Example: `merge_intervals([[1, 2], [4, 5]], gap=2)` returns `[[1, 5]]` (the space between 2 and 4 is 2), while `gap=1` returns `[[1, 2], [4, 5]]`. The input list must still not be changed.
