SELECT customer_id, CAST(julianday(signup_date) - julianday('2026-11-01') AS INTEGER) AS days FROM customers WHERE signup_date >= '2026-07-01' ORDER BY customer_id;
