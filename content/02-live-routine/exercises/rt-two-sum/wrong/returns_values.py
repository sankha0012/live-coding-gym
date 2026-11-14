def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = set()
    for x in nums:
        if target - x in seen:
            return [target - x, x]
        seen.add(x)
    return None
