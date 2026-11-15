from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
_I=SimpleImputer(strategy="median"); _S=StandardScaler()
def build_model():
    return Pipeline([("impute",_I),("scale",_S),("model",LogisticRegression(random_state=0))])
