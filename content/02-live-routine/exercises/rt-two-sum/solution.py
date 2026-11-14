def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for j, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], j]
        seen[x] = j
    return None
