**Why this matters.** Real filters combine several kinds of test: a list of values, a range, and a text pattern. SQL has a short, readable form for each, and knowing them saves a long chain of ORs.

**How we get there.**
1. Cities: `city IN ('Curitiba', 'Belo Horizonte')` replaces two equalities joined by OR.
2. Dates: `signup_date BETWEEN '2026-01-08' AND '2026-03-13'`. BETWEEN includes both ends, which is what "both days included" asks. ISO date text sorts in date order, so the comparison is correct.
3. Names: `name LIKE 'Customer 1%'`. The `%` stands for any run of characters, so this means starts with 'Customer 1'.
4. Join the three tests with AND and select `customer_id, name`.

**Check it.** Both boundary dates are inside the range. A pattern with a trailing `%` can use an index; one with a leading `%` cannot.

**Watch out.** Using `<` and `>` instead of BETWEEN drops the two boundary days, and `LIKE 'Customer 1'` without `%` matches only that exact name.
