"""Quick binary classification metrics (no scikit-learn needed)."""


def precision_recall(y_pred, y_true):
    """Return (precision, recall) for labels 0/1; the positive class is 1."""
    if len(y_pred) != len(y_true):
        raise ValueError("y_pred and y_true must have the same length")
    tp = sum(1 for p, t in zip(y_pred, y_true) if p == 1 and t == 1)
    fp = sum(1 for p, t in zip(y_pred, y_true) if p == 1 and t == 0)
    fn = sum(1 for p, t in zip(y_pred, y_true) if p == 0 and t == 1)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall
