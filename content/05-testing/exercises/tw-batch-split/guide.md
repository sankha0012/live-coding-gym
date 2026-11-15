**Why this matters.** Batching shows up everywhere, from API calls to training loops. Loops like this break at the edges, so the tests live there too.

**How we get there.**
1. Start with an uneven length, `[1, 2, 3, 4, 5]` with size 2. The last batch must be the short `[5]`, so a version that drops the remainder fails.
2. Add an exact multiple, `[1, 2, 3, 4]` with size 2. A loop that runs one step too far adds an empty batch at the end, and the spec says no batch is ever empty.
3. Try a batch size larger than the list, which gives one short batch, and the empty list, which gives `[]`.
4. Test invalid sizes with `pytest.raises(ValueError)`, once for `0` and once for `-1`. A guard written only for zero, or one that silently turns `n` into 1, passes the zero case or hides the error.
5. Check the input list is the same afterwards.

**Check it.** The correct version slices with `range(0, len(items), n)`, which is linear in the list length.

**Watch out.** Testing only zero for the invalid size misses the negative case, and the function then returns nothing useful without any error.
