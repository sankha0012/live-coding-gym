def auc(y, s):
    pos = [si for yi, si in zip(y, s) if yi == 1]
    neg = [si for yi, si in zip(y, s) if yi == 0]
    wins = sum(1 for p in pos for n in neg if p > n)
    return wins / (len(pos) * len(neg))
