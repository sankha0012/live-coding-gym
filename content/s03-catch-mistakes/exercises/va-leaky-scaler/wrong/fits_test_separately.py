from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def prepare(X, y, seed):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = StandardScaler().fit_transform(X_test)
    return X_train_s, X_test_s, y_train, y_test, scaler
