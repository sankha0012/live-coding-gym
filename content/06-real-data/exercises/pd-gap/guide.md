**Why this matters.** "Days since the customer's last order" is a basic feature for churn and retention. The trap is that the file is in no particular order, and the previous order must be the previous one of the same customer.

**How we get there.**
1. Copy the frame and convert `created_at` with `pd.to_datetime`. As text we cannot subtract or sort by time reliably.
2. Sort by `customer_id`, then `created_at`. Now each customer's orders sit together in time order.
3. Take each customer's earlier timestamp with `groupby("customer_id")["created_at"].shift(1)`. The group boundary matters: a first order gets NaT, not the last order of the customer above it.
4. Subtract, and turn the difference into days: `.dt.total_seconds() / 86400`. This gives 1.5 for 36 hours.
5. The sort changed the row order, so `reindex(orders.index)` puts the values back next to the original rows.

**Check it.** A customer's first order is NaN, which is correct. The sort makes it O(n log n).

**Watch out.** Skipping the sort uses file order, and `shift` without `groupby` leaks one customer's last time into the next customer's first order.
