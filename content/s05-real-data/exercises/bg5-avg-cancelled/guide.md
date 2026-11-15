**Why this matters.** The visible example passes, so a quick run says "works". The bug only appears with an input the example does not cover.

**How we get there.**
1. Run the tests. `test_cancelled_with_minutes_not_counted` fails: two delivered orders of 20 and 25 minutes plus a cancelled one of 100 give about 48 instead of 22.5.
2. Reread the prompt and list its rules: delivered only, known time only, `None` when nothing qualifies, a float result.
3. Check each rule against the code. Known time: yes, `is not None`. Empty gives `None`: yes. Float: yes. Delivered only: no `status` check anywhere.
4. Add `o["status"] == "delivered"` to the comprehension condition.
5. Re-run the tests.

**Check it.** Try your own input: a cancelled order with a number, and a list with only cancelled orders.

**Watch out.** Why did the example work? The cancelled order there has `None`, so the `None` check hid the missing status check.
