def PairSum(s):
    nums_text, target_text = s.split("|")
    nums = sorted(set(int(x) for x in nums_text.split(",")))
    target = int(target_text)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return "true"
    return "false"

print(PairSum(input()))
