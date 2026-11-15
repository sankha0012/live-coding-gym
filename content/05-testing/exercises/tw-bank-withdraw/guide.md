**Why this matters.** Money code is where a tiny comparison mistake costs real money. The goal of a test file here is to pin down every line of the rule, so no wrong version can slip through.

**How we get there.**
1. Start with the plain case: `withdraw(100, 30) == 70`. It proves the arithmetic and nothing more.
2. Test the boundary where the amount equals the balance. Taking out everything is allowed and gives `0`, so this catches a `>=` that should be `>`.
3. Test a zero amount and a negative amount in two separate tests. A check for only `amount == 0`, or only `amount < 0`, passes one of them and fails the other.
4. Test the overdraft with `pytest.raises(RuntimeError)`, and give it a case where the amount is just above the balance, like `withdraw(10, 11)`.

**Check it.** Each buggy version fails one of these tests, and the correct one passes all five. The cost is tiny.

**Watch out.** The overdraft test must expect a raise. A version that quietly returns the old balance looks harmless, but in a payments system it hides a failed withdrawal.
