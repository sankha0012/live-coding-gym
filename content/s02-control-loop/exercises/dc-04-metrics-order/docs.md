# quickmetrics: reference

Internal helper for binary classification metrics on plain lists, so notebooks and services do not need scikit-learn for a quick number. The module is `quickmetrics.py`; import it with `from quickmetrics import precision_recall`.

## `precision_recall(y_pred, y_true)`

- `y_pred`: list of predicted labels, each `0` or `1`.
- `y_true`: list of true labels, each `0` or `1`, same length as `y_pred`.

The positive class is `1`.

### Return value

Returns a tuple `(precision, recall)`, in that order, both floats between 0 and 1.

- `precision = tp / (tp + fp)`: of the items predicted positive, the share that really are.
- `recall = tp / (tp + fn)`: of the items that really are positive, the share found.

Nothing is rounded.

### Edge cases

- If the model predicts no positives, `tp + fp` is 0 and `precision` is `0.0`; no error is raised.
- If there are no true positives in `y_true`, `recall` is `0.0`.
- Empty lists return `(0.0, 0.0)`.
- Lists of different lengths raise `ValueError`.

### Gotcha: argument order

The arguments are `(y_pred, y_true)`, the **reverse** of scikit-learn, whose metrics take `(y_true, y_pred)`. Swapping them does not raise an error: the two lists are valid labels either way, so precision and recall silently trade places.

### Example

```python
precision_recall([1, 1, 0, 0], [1, 0, 1, 0])  # (0.5, 0.5)
precision_recall([1, 1, 1, 0], [1, 0, 0, 0])  # (0.333..., 1.0)
```
