import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3],
    "store_id": [10, 10, 20],
    "amount": [100.0, 50.0, 80.0],
})
stores = pd.DataFrame({
    "store_id": [10, 10, 20],
    "city": ["Recife", "Recife", "Sao Paulo"],
})

merged = orders.merge(stores.drop_duplicates("store_id"), on="store_id", how="left", validate="many_to_one")
print(len(orders), len(merged))
print("total before:", orders["amount"].sum())
print("total after:", merged["amount"].sum())

safe = orders.merge(stores.drop_duplicates("store_id"), on="store_id", how="left", validate="many_to_one")
print("safe total:", safe["amount"].sum())

try:
    orders.merge(stores, on="store_id", how="left", validate="many_to_one")
except pd.errors.MergeError:
    print("validate caught duplicate keys")
