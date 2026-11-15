def prf(y, p, t):
    tp = fp = fn = 0
    for yi, pi in zip(y, p):
        pred = 1 if pi >= t else 0
        tp += pred == 1 and yi == 1
        fp += pred == 1 and yi == 0
        fn += pred == 0 and yi == 1
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return prec, rec, (prec + rec) / 2
