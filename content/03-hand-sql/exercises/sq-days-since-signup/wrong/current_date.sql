SELECT customer_id, CAST(julianday('now') - julianday(signup_date) AS INTEGER) AS days FROM customers WHERE signup_date >= '2026-07-01' ORDER BY customer_id;
