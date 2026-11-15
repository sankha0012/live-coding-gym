def running_sum(nums: list) -> list:
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]
    return nums
