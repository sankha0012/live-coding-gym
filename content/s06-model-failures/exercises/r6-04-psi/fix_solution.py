import numpy as np

expected = np.array([0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9])
actual = np.array([0.6, 0.7, 0.7, 0.8, 0.8, 0.9, 0.9, 0.95, 0.95, 0.99])

edges = np.quantile(expected, [0.0, 0.25, 0.5, 0.75, 1.0])
edges[0], edges[-1] = 0.0, 1.0
e = np.histogram(expected, bins=edges)[0] / len(expected)
a = np.histogram(actual, bins=edges)[0] / len(actual)
print("expected share:", e.tolist())
print("actual share:", a.tolist())

eps = 1e-4
e = np.clip(e, eps, None)
a = np.clip(a, eps, None)
psi = float(np.sum((a - e) * np.log(a / e)))
print("psi:", round(psi, 3))
print("drift:", "high" if psi > 0.25 else "ok")
