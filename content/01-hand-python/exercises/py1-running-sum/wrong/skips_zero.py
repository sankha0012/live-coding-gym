def running_sum(nums: list) -> list:
    out, t = [], 0
    for x in nums:
        t += x
        if x:
            out.append(t)
    return out
