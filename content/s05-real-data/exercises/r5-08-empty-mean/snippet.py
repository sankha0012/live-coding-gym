import pandas as pd

orders = pd.DataFrame({"city": ["Recife", "Recife"], "amount": [40.0, 60.0]})

def avg_ticket(df, city):
    return df.loc[df["city"] == city, "amount"].mean()

print(avg_ticket(orders, "Recife"))
rio = avg_ticket(orders, "Rio")
print(rio)
print(f"Rio ticket: {rio:.2f}")
print(rio > 50, rio <= 50)
print(round(rio, 1) == rio)

def safe_avg(df, city, default=0.0):
    sub = df.loc[df["city"] == city, "amount"]
    return default if sub.empty else sub.mean()

print(safe_avg(orders, "Rio"))
