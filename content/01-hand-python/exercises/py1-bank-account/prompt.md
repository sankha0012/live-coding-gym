Write a class `BankAccount` that starts at balance 0.
- `deposit(amount)` adds money. `amount` must be above 0, otherwise raise `ValueError`.
- `withdraw(amount)` removes money. `amount` must be above 0 and not more than the balance, otherwise raise `ValueError`. Withdrawing exactly the whole balance is allowed.
- `balance` is a read-only property. Setting it raises `AttributeError`.
A failed call must leave the balance unchanged.
