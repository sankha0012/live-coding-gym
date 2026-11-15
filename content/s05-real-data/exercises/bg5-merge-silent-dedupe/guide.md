**Why this matters.** A join that quietly changes the data is one of the most common sources of wrong numbers. Here the assistant made the symptom disappear, which looks like robustness but is the opposite.

**How we get there.**
1. Run the tests. `test_duplicate_restaurant_key_raises` fails with "DID NOT RAISE".
2. Read the prompt again: raise `ValueError` when the merged frame has a different row count. Then search the code for `raise`. There is none.
3. Find the line that prevents the error from ever happening: `drop_duplicates("restaurant_id")` on `restaurants`.
4. Fix: merge the original frames with `how="left"`, then `if len(merged) != len(orders): raise ValueError(...)`.
5. Re-run the tests. The case with a duplicate key that no order uses must still pass: it does not change the row count, so it is not an error.

**Check it.** Add a duplicate restaurant row by hand and confirm the error message shows both counts.

**Watch out.** Checking `restaurants["restaurant_id"].duplicated().any()` is a different rule: it fails even when no order uses the duplicated key.
