import pandas as pd

df = pd.DataFrame({
    "age": [30.0, None, 50.0, None],
    "income": [100.0, 200.0, None, 400.0],
})

filled = df.fillna(df["age"].mean())
print(filled)

dropped = df.dropna(subset=["age"])
print(len(dropped), list(dropped.index))
print(df["age"].isna().sum())
