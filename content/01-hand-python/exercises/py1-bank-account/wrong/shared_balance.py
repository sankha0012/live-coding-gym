class BankAccount:
    _b = [0]
    def deposit(self, amount):
        if amount <= 0: raise ValueError
        self._b[0] += amount
    def withdraw(self, amount):
        if amount <= 0 or amount > self._b[0]: raise ValueError
        self._b[0] -= amount
    @property
    def balance(self): return self._b[0]
