y_true = [0] * 95 + [1] * 5
y_pred = [0] * 100

correct = sum(t == p for t, p in zip(y_true, y_pred))
print("accuracy:", correct / len(y_true))

tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
print("recall:", tp / (tp + fn))

predicted_pos = sum(y_pred)
precision = tp / predicted_pos if predicted_pos else 0.0
print("precision:", precision)
print("positives caught:", tp, "of", tp + fn)
