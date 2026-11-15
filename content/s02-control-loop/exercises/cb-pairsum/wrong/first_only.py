def PairSum(s):
    nums_text, target_text = s.split("|")
    nums = [int(x) for x in nums_text.split(",")]
    target = int(target_text)
    return "true" if any(nums[0] + y == target for y in nums[1:]) else "false"

print(PairSum(input()))
