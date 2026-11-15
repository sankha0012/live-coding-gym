def SumByKey(s):
    totals = {}
    for piece in s.split(","):
        key, value = piece.split(":")
        totals[key] = totals.get(key, 0) + int(value)
    return ",".join(f"{k}:{v}" for k, v in totals.items())

print(SumByKey(input()))
