from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler


def cv_accuracy(X, y):
    Xs = StandardScaler().fit_transform(X)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(LogisticRegression(max_iter=1000, random_state=0), Xs, y, cv=cv, scoring="accuracy")
    return float(scores.mean())
