import pandas as pd


def leaky_features(features: pd.DataFrame, label: pd.Series, threshold: float = 0.95) -> list[str]:
    corr = features.corrwith(label).abs()
    return sorted(str(c) for c in corr.index[corr > threshold])
