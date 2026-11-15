def withdraw(balance, amount):
    if amount == 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise RuntimeError("insufficient funds")
    return balance - amount
