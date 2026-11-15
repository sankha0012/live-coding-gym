**Why this matters.** "Second highest" is a famous interview question. The trap is ties: if the top value appears twice, the second row is still the top value, not the second highest one.

**How we get there.**
1. The highest subtotal is easy: `SELECT MAX(subtotal) FROM orders`.
2. Use that as a scalar subquery and keep only rows strictly below it: `WHERE subtotal < (SELECT MAX(subtotal) FROM orders)`.
3. Take the `MAX` of what is left. It is the largest value below the top, which is exactly the second highest distinct value.

**Check it.** The strict `<` is what makes ties harmless, since every copy of the top value is removed. If there is only one distinct value, the result is NULL. The cost is two scans. `DENSE_RANK() = 2` does the same and also works for the third, fourth and so on.

**Watch out.** Using `ORDER BY subtotal DESC LIMIT 1 OFFSET 1`, which returns the second row, and so the top value again when it is tied. Here the maximum is unique, so it happens to give the same number, but it is wrong in general.
