def PairSum(s):
    nums_text, target_text = s.split("|")
    nums = [int(x) for x in nums_text.split(",")]
    target = int(target_text)
    seen = set()
    for x in nums:
        if target - x and target - x in seen:
            return "true"
        seen.add(x)
    return "false"

print(PairSum(input()))
