from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_model():
    return Pipeline([
        ("scale", StandardScaler()),
        ("impute", SimpleImputer(strategy="median")),
        ("model", LogisticRegression(random_state=0)),
    ])
