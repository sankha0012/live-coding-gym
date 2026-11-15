def SumByKey(s):
    totals = {}
    for piece in s.split(","):
        key, value = piece.split(":")
        totals[key] = totals.get(key, 0) + int(value)
    return ",".join(f"{k}:{totals[k]}" for k in sorted(totals))

print(SumByKey(input()))
