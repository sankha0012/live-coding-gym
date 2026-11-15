state = {"model": None}


def predict(features):
    return state["model"].predict([features])[0]


def health():
    try:
        predict([1.0, 2.0])
    except Exception:
        pass
    return {"status": "ok"}


print(health())
try:
    predict([1.0, 2.0])
except Exception as exc:
    print(type(exc).__name__)
print(health()["status"] == "ok")
