**Why this matters.** A bank account is the standard small class problem. The point is protecting an invariant: the balance must never be wrong, even when a caller makes a mistake.

**How we get there.**
1. In `__init__`, store the money in a private attribute, `self._balance = 0`.
2. In `deposit`, validate first: if `amount <= 0`, raise `ValueError`. Only after the check do we do `self._balance += amount`.
3. In `withdraw`, do two checks, a non-positive amount and `amount > self._balance`, each raising `ValueError`. Then subtract.
4. Expose the balance with `@property`. With a getter and no setter, assigning to `balance` raises `AttributeError` by itself.

**Check it.** Because every check comes before the change, a failed call leaves the balance as it was. Withdrawing exactly the whole balance is allowed, because we only reject when the amount is strictly greater. Everything is O(1).

**Watch out.** Using `>=` in the overdraft check makes it impossible to empty an account, and a plain public attribute lets anyone set the balance directly.
