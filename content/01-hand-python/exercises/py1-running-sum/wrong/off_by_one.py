def running_sum(nums: list) -> list:
    out = []
    total = 0
    for x in nums:
        out.append(total)
        total += x
    return out
