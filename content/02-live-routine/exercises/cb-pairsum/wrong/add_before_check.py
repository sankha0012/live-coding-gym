def PairSum(s):
    nums_text, target_text = s.split("|")
    nums = [int(x) for x in nums_text.split(",")]
    target = int(target_text)
    seen = set()
    for x in nums:
        seen.add(x)
        if target - x in seen:
            return "true"
    return "false"

print(PairSum(input()))
