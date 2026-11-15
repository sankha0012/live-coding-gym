**Why this matters.** Deduplication that keeps the wrong version looks fine on a quick check: one row per key, no errors. The data is just silently stale.

**How we get there.**
1. Run the tests. `test_latest_row_wins_not_the_last_in_file` fails: for id 1 you get `a2` instead of `a3`.
2. Read the function. `time_col` is a parameter but never appears in the body. A function that ignores one of its inputs is suspect.
3. `drop_duplicates(key, keep="last")` keeps the last row in the current row order. The test frame is deliberately not in time order, so "last in file" and "newest" differ.
4. Fix: `df.sort_values(time_col, kind="stable")` before `drop_duplicates`. A stable sort keeps ties in input order, so the later input row stays last and wins.
5. Re-run the tests, including the tie tests.

**Check it.** Print the frame for one key before and after and compare the timestamps with your eyes.

**Watch out.** Without `kind="stable"` the default sort may reorder equal times, which breaks the tie rule on large inputs.
