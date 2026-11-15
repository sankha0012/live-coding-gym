from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_model():
    return Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(random_state=0)),
    ])
