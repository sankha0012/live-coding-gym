**Why this matters.** Revenue reports that include cancelled orders look plausible and are wrong, and nothing in SQL warns you.

**How we get there.**
1. Read the prompt: delivered orders only. Look for `status` in the query. It is not there.
2. Run `SELECT status, COUNT(*) FROM orders GROUP BY status` to see how many cancelled rows were being counted.
3. Add `WHERE o.status = 'delivered'` between the JOIN and the GROUP BY.
4. Run again. Orders and revenue go down for each cuisine, and the order of cuisines can change.

**Check it.** Pick one cuisine and sum its delivered subtotals by hand with a simple query. It must equal the revenue shown.

**Watch out.** Filtering with HAVING on status would not work: status is not an aggregate, and the filter must happen before the sum.
