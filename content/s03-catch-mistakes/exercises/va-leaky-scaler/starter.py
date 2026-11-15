from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def prepare(X, y, seed):
    """Split, then scale features using statistics from the train rows only.

    Returns (X_train_s, X_test_s, y_train, y_test, scaler).
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train_s, X_test_s, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.25, random_state=seed
    )
    return X_train_s, X_test_s, y_train, y_test, scaler
