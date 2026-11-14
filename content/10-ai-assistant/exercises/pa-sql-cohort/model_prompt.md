Write one SQLite query for monthly signup cohort retention.

Tables: `customers(customer_id, signup_date TEXT 'YYYY-MM-DD', ...)` and `orders(order_id, customer_id, created_at TEXT 'YYYY-MM-DD HH:MM:SS', status, ...)`.

Definitions:
- Cohort month = `strftime('%Y-%m', signup_date)`.
- Order month = `strftime('%Y-%m', created_at)`. Count only orders with `status = 'delivered'`.
- Month offset = number of months between the cohort month and the order month, 0 for the signup month itself. Compute it from year and month numbers, not by subtracting strings.
- Ignore orders placed before the signup month.

Output columns: `cohort_month`, `month_offset`, `active_customers` (count of DISTINCT customers with a delivered order in that offset), `cohort_size` (all customers who signed up that month, including those who never ordered), `retention` (active_customers / cohort_size as a real number rounded to 3 decimals, so use `* 1.0`). Order by cohort_month, month_offset.

Edge cases: customers with no orders still count in cohort_size. A customer with several orders in a month counts once. Customers with a NULL signup_date are excluded.

Please use CTEs, make the query readable, then explain the join choice (why not only an inner join) and suggest two sanity checks I can run, such as retention at offset 0 not exceeding 1.
