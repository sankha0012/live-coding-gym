def normalise(values, scale=1.0):
    if not values:
        return
    top = max(values)
    return [round(v / top * scale, 2) for v in values]


def describe(values, label="data"):
    result = normalise(values, scale=10)
    if result is None:
        return f"{label}: nothing to scale"
    return f"{label}: {result}"


print(normalise([2, 4, 8]))
print(normalise([2, 4, 8], 100))
print(normalise([]))
print(describe([1, 5]))
print(describe([], label="empty"))
x = normalise([3])
print(x)
