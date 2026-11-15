import pandas as pd

df = pd.DataFrame({
    "city": ["SP", "SP", "RJ", "RJ", "RJ", "BH"],
    "value": [10.0, 30.0, 20.0, None, 40.0, 50.0],
})

out = df.groupby("city").agg(
    orders=("value", "size"),
    known=("value", "count"),
    avg=("value", "mean"),
    total=("value", "sum"),
).reset_index()

print(out)
print(out["orders"].sum(), out["known"].sum())
