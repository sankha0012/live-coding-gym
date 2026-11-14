def binary_metrics(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError("length mismatch")
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    n = len(y_true)
    recall = tp / (tp + fp) if tp + fp else 0.0
    precision = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"accuracy": sum(t == p for t, p in zip(y_true, y_pred)) / n if n else 0.0,
            "precision": precision, "recall": recall, "f1": f1}
