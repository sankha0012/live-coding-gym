class BankAccount:
    def __init__(self): self._balance = 0
    def deposit(self, amount):
        if amount <= 0: raise ValueError
        self._balance += amount
    def withdraw(self, amount):
        if amount > self._balance: raise ValueError
        self._balance -= amount
    @property
    def balance(self): return self._balance
