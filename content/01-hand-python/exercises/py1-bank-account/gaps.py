class BankAccount:
    def __init__(self):
        self._balance = ____

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ____("amount must be positive")
        if amount ____ self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount

    @____
    def balance(self):
        return self._balance
