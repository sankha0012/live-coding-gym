**Why this matters.** A city dashboard needs two different answers: how often orders are late, and how late they are when they are late. They look alike but use different denominators, and mixing them is the classic mistake.

**How we get there.**
1. Keep delivered orders and take a `.copy()`, so we do not change the caller's frame.
2. Merge in the city with a left join on `restaurant_id`, bringing only that column across.
3. Add a boolean `late` column, `actual_minutes > promised_minutes`. The mean of a True/False column is exactly the share of True, so that is `late_rate`.
4. Add `minutes_late`, the difference clipped at zero, so early orders count as 0 rather than negative.
5. One `groupby("city").agg(...)` with named aggregation: the count of order ids, the mean of `late`, and `avg_late` as the mean of only the rows above zero, `s[s > 0].mean()`.

**Check it.** A city with no late orders gets an empty selection, and the mean of nothing is NaN, as the spec asks. It is one pass, so linear time.

**Watch out.** A plain mean of `minutes_late` includes the on-time rows, which dilutes the number toward zero.
