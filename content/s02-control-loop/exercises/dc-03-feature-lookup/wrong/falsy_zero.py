from featurestore import get_features


def feature_row(keys, fallback):
    feats = get_features(keys)
    return [feats.get(k) or fallback for k in keys]
