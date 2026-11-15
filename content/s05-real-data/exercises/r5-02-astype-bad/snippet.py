import pandas as pd

raw = pd.Series(["12", "7", "n/a", "30"], name="items")

try:
    items = raw.astype(int)
except ValueError as err:
    print("astype failed:", err)

items = pd.to_numeric(raw, errors="coerce")
print(items.tolist())
print("bad rows:", int(items.isna().sum()))
print(items.dtype)
print("mean:", items.mean())
