models = ["svm", "tree", "logreg", "knn"]
scores = [0.81, 0.90, 0.81, 0.77]

pairs = list(zip(models, scores))
print(pairs)

ranked = sorted(pairs, key=lambda p: (-p[1], p[0]))
for rank, (name, score) in enumerate(ranked, start=1):
    print(rank, name, score)

by_name_length = sorted(models, key=lambda m: len(m))
print(by_name_length)
print(models)
