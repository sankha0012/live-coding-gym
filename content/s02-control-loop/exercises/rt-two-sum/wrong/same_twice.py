def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for j, x in enumerate(nums):
        seen[x] = j
        if target - x in seen:
            return [seen[target - x], j]
    return None
