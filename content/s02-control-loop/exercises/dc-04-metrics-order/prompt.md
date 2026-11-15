Write `report(y_true, y_pred)`, which follows the scikit-learn convention of taking `y_true` first. It returns a dict `{"precision": ..., "recall": ..., "f1": ...}`, where `f1 = 2 * p * r / (p + r)`, and `f1` is `0.0` when `p + r` is 0.

Use the `quickmetrics` helper for precision and recall. Documentation is available below the task, consult it. Check the order of the helper's arguments and of the values it returns.
