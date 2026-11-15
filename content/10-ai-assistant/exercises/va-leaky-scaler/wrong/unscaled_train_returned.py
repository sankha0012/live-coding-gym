from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def prepare(X, y, seed):
    a,b,c,d = train_test_split(X, y, test_size=0.25, random_state=seed)
    s=StandardScaler().fit(a); return a, s.transform(b), c, d, s
