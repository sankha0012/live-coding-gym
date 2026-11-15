**Why this matters.** In an anti-join, the condition in the ON clause decides what counts as a match. Any extra condition there quietly redefines "has an order".

**How we get there.**
1. Run the query and read the prompt again: customers with no order of any status.
2. Take one customer from the result and look at their rows in `orders`. Customers like 900001 have a cancelled order, so they should not be listed.
3. Find the cause: `AND o.status = 'delivered'` in the ON clause. Cancelled orders no longer match, so those customers get NULL order columns.
4. Delete that condition. The join now matches every order a customer has.
5. Keep `WHERE c.city = 'Curitiba' AND o.order_id IS NULL`.

**Check it.** Compare your row count with the reference. The customers with only cancelled orders must be gone from the list.

**Watch out.** If you really wanted "no delivered order", that is a different question (see the NOT EXISTS exercise), and the right tool there is NOT EXISTS with the status inside the subquery.
