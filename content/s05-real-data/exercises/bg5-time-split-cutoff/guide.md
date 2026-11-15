**Why this matters.** A boundary that belongs to both sides is a classic off-by-one. On real data with many timestamps it rarely shows up, so the average metrics look fine while the split is still wrong.

**How we get there.**
1. Run the tests. `test_row_exactly_at_cutoff_goes_to_test` fails: the row at `2026-10-01 00:00:00` is in both train and test.
2. Read the two conditions. `ts <= c` for train and `ts >= c` for test. Both include `==`.
3. Fix with one mask: `before = ts < pd.Timestamp(cutoff)`, then `orders[before]` and `orders[~before]`. The negation guarantees every row is in exactly one side.
4. Re-run the tests. Check the sizes as well: `len(train) + len(test) == len(orders)`.

**Check it.** Build a tiny frame with one row exactly at the cutoff and look at both outputs.

**Watch out.** Comparing the text column directly can work by luck for this format, but converting with `pd.to_datetime` is the safe way. Do not overwrite `created_at` in the output, the spec says to leave it as it came.
