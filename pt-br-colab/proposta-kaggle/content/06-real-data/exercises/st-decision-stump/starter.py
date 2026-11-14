def fit_stump(xs, ys):
    raise NotImplementedError


def predict(model, x):
    raise NotImplementedError


if __name__ == "__main__":
    import random

    rng = random.Random(0)
    xs = [rng.uniform(0, 20) for _ in range(10)]
    ys = [int(x > 12) for x in xs]
    print(list(zip(xs, ys)))
