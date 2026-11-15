from quickmetrics import precision_recall


def report(y_true, y_pred):
    p, r = precision_recall(y_pred, y_true)
    f1 = 2 * p * r / (p + r)
    return {"precision": p, "recall": r, "f1": f1}
