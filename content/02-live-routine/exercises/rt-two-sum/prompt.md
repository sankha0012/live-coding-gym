Write `two_sum(nums: list[int], target: int) -> list[int] | None`. Return the indices `[i, j]` with `i < j` of two different positions whose numbers add up to `target`. Use one pass with a dict. You may not use the same position twice. If no pair exists, return `None`. An empty list returns `None`. If several pairs exist, return the pair with the smallest `j`. If several positions `i` fit that `j`, use the largest `i`. So `two_sum([2, 2, 8], 10)` returns `[1, 2]`.

Example: `two_sum([2, 7, 11, 15], 9)` returns `[0, 1]`.
