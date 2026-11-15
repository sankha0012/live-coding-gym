import joblib


def save_and_load(model, path):
    joblib.dump(model, path)
    return joblib.load(path)
