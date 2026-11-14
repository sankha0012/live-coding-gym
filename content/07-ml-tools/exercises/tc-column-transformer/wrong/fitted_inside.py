from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import pandas as pd
def build_preprocessor(n,c):
    return ColumnTransformer([("num",StandardScaler(),n),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),c)]).fit(pd.DataFrame({"age":[1.0,2.0],"fee":[1.0,2.0],"city":["a","b"]}))
