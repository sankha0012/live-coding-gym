registry = {
    ("churn", "1.0"): "model-churn-1.0",
    ("churn", "1.1"): "model-churn-1.1",
    ("churn", "latest"): "model-churn-1.1",
}


def load_model(name, version):
    return registry[(name, version)]


print(load_model("churn", "1.0"))
print(load_model("churn", "latest"))
try:
    load_model("fraud", "1.0")
except KeyError as exc:
    print("KeyError", exc)
