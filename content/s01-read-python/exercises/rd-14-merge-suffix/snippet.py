import pandas as pd

users = pd.DataFrame({"id": [1, 2, 3], "score": [0.5, 0.7, 0.9]})
labels = pd.DataFrame({"id": [1, 1, 3, 4], "score": [1, 0, 1, 0]})

out = users.merge(labels, on="id", how="left", suffixes=("_pred", "_true"))
print(out)
print(len(users), len(out))
print(out["score_true"].isna().sum())
print(out["score_true"].dtype)
print(labels["id"].is_unique)
