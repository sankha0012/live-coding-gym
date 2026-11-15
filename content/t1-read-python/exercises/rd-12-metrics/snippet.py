y_true = [1, 0, 1, 1, 0, 0, 1, 0]
y_pred = [1, 0, 0, 1, 1, 0, 1, 0]

tp = fp = fn = tn = 0
for t, p in zip(y_true, y_pred):
    if p == 1 and t == 1:
        tp += 1
    elif p == 1 and t == 0:
        fp += 1
    elif p == 0 and t == 1:
        fn += 1
    else:
        tn += 1

precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0
accuracy = (tp + tn) / len(y_true)
print(tp, fp, fn, tn)
print(f"precision={precision:.2f} recall={recall:.2f} accuracy={accuracy:.2f}")
