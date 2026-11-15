from featurestore import get_features


def feature_row(keys, fallback):
    feats = get_features(keys, default=fallback)
    return [feats[k] for k in keys]
