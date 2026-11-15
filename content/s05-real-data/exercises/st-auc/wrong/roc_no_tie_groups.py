def auc(y, s):
    order = sorted(range(len(s)), key=lambda i: -s[i])
    P = sum(1 for v in y if v == 1); N = len(y) - P
    tp = fp = 0; area = 0.0
    for i in order:
        if y[i] == 1:
            tp += 1
        else:
            fp += 1
            area += tp / P / N
    return area
