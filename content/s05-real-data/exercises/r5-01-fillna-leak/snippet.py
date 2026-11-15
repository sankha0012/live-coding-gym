import pandas as pd

df = pd.DataFrame({
    "day": [1, 2, 3, 4, 5, 6],
    "basket": [10.0, None, 12.0, 14.0, None, 90.0],
})
train = df[df["day"] <= 4].copy()
test = df[df["day"] > 4].copy()

# fill gaps with the mean of the whole frame
fill = df["basket"].mean()
train["basket"] = train["basket"].fillna(fill)
test["basket"] = test["basket"].fillna(fill)
print("fill used:", fill)
print(train["basket"].tolist())
print(test["basket"].tolist())

# fill gaps with the mean of the training rows only
fill_train = df.loc[df["day"] <= 4, "basket"].mean()
print("train-only fill:", fill_train)
