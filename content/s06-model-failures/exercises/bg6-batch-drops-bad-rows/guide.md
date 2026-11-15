**Why this matters.** Batch scoring returns results by position. If a failure shortens the list, the caller silently pairs scores with the wrong rows, which is worse than a crash.

**How we get there.**
1. Run the tests. The order and length tests fail.
2. Reproduce with rows priced `[1, -5, 3]` and a `score_fn` that doubles the price and raises `ValueError` for negatives. The scores come back as `[2, 6]` and the errors list says index 1.
3. Count: three rows in, two scores out. Find where a score is added: only in the `try`.
4. In the `except` branch, add `scores.append(None)` before recording the error.
5. Run the tests again. All pass, including the one with two bad rows in a four-row batch.

**Check it.** `len(result["scores"]) == len(rows)` must always hold. That one assertion would have caught this.

**Next time.** For any function that returns "one result per input", test the length and the positions with a failing item in the middle.

**Watch out.** Keep `except Exception`: catching `BaseException` would also swallow `KeyboardInterrupt`.
