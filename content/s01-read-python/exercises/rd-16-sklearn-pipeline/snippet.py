from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X = [[1.0, 100.0], [2.0, 110.0], [3.0, 120.0], [4.0, 300.0], [5.0, 310.0], [6.0, 320.0]]
y = [0, 0, 0, 1, 1, 1]

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(random_state=0)),
])
pipe.fit(X, y)

print(pipe.predict([[1.5, 105.0], [5.5, 315.0]]))
print(round(float(pipe.score(X, y)), 2))
print(pipe.named_steps["scale"].mean_.round(2))
print(list(pipe.named_steps))
