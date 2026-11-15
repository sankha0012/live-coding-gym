def two_sum(nums, target):
    seen = {}
    for j, x in enumerate(nums):
        if x > 0 and target - x in seen:
            return [seen[target - x], j]
        seen[x] = j
    return None
