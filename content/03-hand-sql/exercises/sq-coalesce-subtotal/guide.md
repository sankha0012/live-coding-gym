**Why this matters.** Missing data and arithmetic do not mix. If a value is NULL, any sum that includes it becomes NULL, so a total quietly disappears instead of raising an error.

**How we get there.**
1. We only want the problem rows, so start with `FROM orders WHERE subtotal IS NULL`. We use `IS NULL` because `= NULL` is never true.
2. Compute the total as `subtotal + delivery_fee`. For these rows that is NULL plus a number, which is NULL: exactly the bug.
3. Replace the missing value with `COALESCE(subtotal, 0)`. COALESCE returns its first argument that is not NULL.
4. Name the column `total` and sort by `order_id`.

The key line is `COALESCE(subtotal, 0) + delivery_fee AS total`.

**Check it.** Every returned row has a NULL subtotal, so the total equals the delivery fee. That is a good sanity check on the result. It is one scan of the table.

**Watch out.** Treating a missing subtotal as 0 is a business decision, not a fact; and writing `subtotal = NULL` returns no rows at all.
