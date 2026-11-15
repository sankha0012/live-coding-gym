def PairSum(s):
    parts = s.split("|")
    nums = [int(x) for x in parts[0].split(",")]
    target = int(parts[1])
    distinct = len(parts) == 3 and parts[2] == "distinct"
    seen = set()
    for x in nums:
        if target - x in seen and not (distinct and target - x == x):
            return "true"
        seen.add(x)
    return "false"

print(PairSum(input()))
