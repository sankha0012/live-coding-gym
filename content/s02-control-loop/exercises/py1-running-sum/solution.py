def running_sum(nums: list) -> list:
    out = []
    total = 0
    for x in nums:
        total += x
        out.append(total)
    return out
