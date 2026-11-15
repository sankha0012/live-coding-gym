def auc(y, s):
    order = sorted(range(len(s)), key=lambda i: s[i])
    rank = {i: r + 1 for r, i in enumerate(order)}
    n1 = sum(1 for v in y if v == 1)
    n0 = len(y) - n1
    r1 = sum(rank[i] for i in range(len(y)) if y[i] == 1)
    return (r1 - n1 * (n1 + 1) / 2) / (n1 * n0)
