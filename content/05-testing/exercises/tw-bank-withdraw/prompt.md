# Test `withdraw`

`withdraw(balance, amount)` returns the new balance after taking `amount` out of `balance`.

- Normal case: `withdraw(100, 30)` returns `70`.
- Withdrawing exactly the whole balance is allowed and returns `0`.
- If `amount` is zero or negative, it raises `ValueError`.
- If `amount` is greater than `balance`, it raises `RuntimeError`. It must not return a balance in that case.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import withdraw
