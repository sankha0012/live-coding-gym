def PairSum(s):
    nums_text, target_text = s.split("|")
    nums = [int(x) for x in nums_text.split(",")]
    target = int(target_text)
    return "true" if any(nums[i] + nums[i + 1] == target for i in range(len(nums) - 1)) else "false"

print(PairSum(input()))
