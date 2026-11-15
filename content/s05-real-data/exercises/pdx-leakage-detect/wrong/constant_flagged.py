import numpy as np
import pandas as pd

def leaky_features(features, label, threshold=0.95):
    corr = features.corrwith(label).abs().fillna(1.0)
    return sorted(str(c) for c in corr.index[corr > threshold])
