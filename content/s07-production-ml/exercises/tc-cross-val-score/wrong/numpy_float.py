import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def cv_accuracy(X,y):
    m=Pipeline([("s",StandardScaler()),("m",LogisticRegression(max_iter=1000,random_state=0))])
    return cross_val_score(m,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=42)).mean()
