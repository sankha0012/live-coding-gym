**Why this matters.** Date arithmetic is full of small traps. Here the biggest one is hidden: using the current date makes the answer change every day, so no one can check it. We pin the date to a fixed value.

**How we get there.**
1. Filter first: `FROM customers WHERE signup_date >= '2026-07-01'`. ISO dates ('YYYY-MM-DD') compare correctly as plain text.
2. SQLite has no direct date subtraction, so convert each date to a day number with `julianday(...)`.
3. Subtract: `julianday('2026-11-01') - julianday(signup_date)` is the number of days, possibly with a fraction.
4. Wrap it in `CAST(... AS INTEGER)` to get whole days.
5. Sort by `customer_id`.

**Check it.** For two plain dates the difference is already a whole number, and the cast keeps it clean. It is one scan, linear. In Postgres the same idea is just subtracting two dates.

**Watch out.** Writing `'now'` instead of the fixed date makes the result drift every day.
