import pandas as pd

df = pd.DataFrame({
    "user": ["a", "b", "c", "d", "e"],
    "income": [4000.0, None, 5200.0, None, 4800.0],
})

filled = df["income"].fillna(0)
print("mean raw:", round(df["income"].mean(), 1))
print("mean filled:", round(filled.mean(), 1))
print("low income:", int((filled < 2000).sum()))

median = df["income"].median()
safe = df["income"].fillna(median)
print("low income (median fill):", int((safe < 2000).sum()))
print("missing:", int(df["income"].isna().sum()))
