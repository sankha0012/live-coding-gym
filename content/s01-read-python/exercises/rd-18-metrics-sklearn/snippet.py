from sklearn.metrics import precision_score, recall_score, roc_auc_score

y_true = [1, 0, 1, 1, 0, 0, 1, 0]
y_prob = [0.9, 0.4, 0.35, 0.8, 0.5, 0.1, 0.6, 0.3]
y_pred = [1 if p >= 0.5 else 0 for p in y_prob]

print(y_pred)
print(round(precision_score(y_true, y_pred), 3))
print(round(recall_score(y_true, y_pred), 3))
print(round(roc_auc_score(y_true, y_prob), 3))
print(round(roc_auc_score(y_true, y_pred), 3))
