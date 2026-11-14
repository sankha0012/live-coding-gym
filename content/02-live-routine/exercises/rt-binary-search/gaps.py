def first_index(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo ____ hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = ____
        else:
            hi = ____
    return lo if lo < len(nums) and nums[lo] == target else -1
