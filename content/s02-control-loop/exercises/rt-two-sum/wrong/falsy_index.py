def two_sum(nums, target):
    seen = {}
    for j, x in enumerate(nums):
        if seen.get(target - x):
            return [seen[target - x], j]
        seen[x] = j
    return None
