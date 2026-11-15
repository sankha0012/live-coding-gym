from sklearn.model_selection import train_test_split

X = list(range(10))
y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

a, b, ya, yb = train_test_split(X, y, test_size=0.3, random_state=42)
c, d, yc, yd = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

print(len(a), len(b))
print(sorted(b), sum(yb))
print(sorted(d), sum(yd))
print(sorted(a + b) == X)
