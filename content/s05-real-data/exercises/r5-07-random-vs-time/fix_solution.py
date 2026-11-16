import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.DataFrame({"day": range(20)})
df["sales"] = 100 + 10 * df["day"]          # sales keep growing

rand_train, rand_test = train_test_split(df, test_size=0.25, shuffle=False)
time_train, time_test = df.iloc[:15], df.iloc[15:]

for name, tr, te in [("random", rand_train, rand_test), ("time", time_train, time_test)]:
    gap = abs(te["sales"].mean() - tr["sales"].mean())
    leak = bool((tr["day"] > te["day"].min()).any())
    print(f"{name}: test days {sorted(te['day'].tolist())}")
    print(f"{name}: train mean={tr['sales'].mean():.1f} test mean={te['sales'].mean():.1f} gap={gap:.1f}")
    print(f"{name}: train has days after first test day: {leak}")
