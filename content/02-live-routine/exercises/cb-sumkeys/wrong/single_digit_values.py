def SumByKey(s):
    totals = {}
    for piece in s.split(","):
        totals[piece[0]] = totals.get(piece[0], 0) + int(piece[2])
    return ",".join(f"{k}:{totals[k]}" for k in sorted(totals))

print(SumByKey(input()))
