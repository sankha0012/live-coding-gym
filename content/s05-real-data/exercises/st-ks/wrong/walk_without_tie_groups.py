def ks(y, s):
    ng = sum(1 for v in y if v == 0); nb = len(y) - ng
    cg = cb = 0
    best = 0.0
    for i in sorted(range(len(s)), key=lambda i: s[i]):
        if y[i] == 0:
            cg += 1
        else:
            cb += 1
        best = max(best, abs(cg / ng - cb / nb))
    return best
