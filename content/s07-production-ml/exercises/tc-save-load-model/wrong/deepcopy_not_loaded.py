import joblib, copy, pickle

def save_and_load(m,p):
    joblib.dump(m,p); return copy.deepcopy(m)
