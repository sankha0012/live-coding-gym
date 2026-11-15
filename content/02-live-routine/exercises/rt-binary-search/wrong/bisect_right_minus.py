import bisect

def first_index(nums, target):
    i = bisect.bisect_right(nums, target) - 1
    return i if i >= 0 and nums[i] == target else -1
