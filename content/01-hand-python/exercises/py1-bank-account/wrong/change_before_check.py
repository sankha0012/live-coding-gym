class BankAccount:
    def __init__(self): self._balance = 0
    def deposit(self, amount):
        self._balance += amount
        if amount <= 0:
            raise ValueError
    def withdraw(self, amount):
        self._balance -= amount
        if amount <= 0 or self._balance < 0:
            raise ValueError
    @property
    def balance(self): return self._balance
