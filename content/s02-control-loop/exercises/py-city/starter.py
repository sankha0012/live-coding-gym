ORDERS = [
    {"city": "SP", "status": "delivered", "subtotal": 50.0, "fee": 5.0},
    {"city": "SP", "status": "cancelled", "subtotal": 30.0, "fee": 5.0},
    {"city": "RJ", "status": "delivered", "subtotal": None, "fee": 7.5},
    {"city": "RJ", "status": "delivered", "subtotal": 20.0, "fee": 0.0},
]

def gmv_by_city(orders):
    pass

print(gmv_by_city(ORDERS))
