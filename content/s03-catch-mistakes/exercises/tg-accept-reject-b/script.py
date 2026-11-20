# evaluate.py: the script you asked the assistant to change. This is the code BEFORE its changes.
# The task: make test_precision pass, and make the decision threshold configurable.
THRESHOLD = 0.5


def precision(preds, labels):
    return sum(preds) / len(preds)


def classify(prob):
    return int(prob >= THRESHOLD)


def evaluate(preds, labels):
    p = precision(preds, labels)
    return {"precision": p, "n": len(preds)}


# tests/test_evaluate.py
def test_precision():
    preds = [1, 1, 0, 1]
    labels = [1, 0, 0, 1]
    assert precision(preds, labels) == 2 / 3
