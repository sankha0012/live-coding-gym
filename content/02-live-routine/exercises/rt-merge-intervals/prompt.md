Write `merge_intervals(intervals: list[list[int]]) -> list[list[int]]`. Each interval is `[start, end]` with `start <= end`, closed on both sides. Merge every interval that overlaps or touches another (`[1, 2]` and `[2, 3]` become `[1, 3]`). The input may be unsorted. Return the merged intervals sorted by start. An empty list returns `[]`. Do not change the input list.

Example: `merge_intervals([[8, 10], [1, 3], [2, 6]])` returns `[[1, 6], [8, 10]]`.
