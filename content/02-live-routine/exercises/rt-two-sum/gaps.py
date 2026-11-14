def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for j, x in ____(nums):
        if target - x in ____:
            return [seen[target - x], j]
        seen[x] = ____
    return None
