import joblib


def save_and_load(model, path):
    joblib.dump(model.steps[-1][1], path)
    return joblib.load(path)
