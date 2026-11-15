SELECT customer_id, CAST(julianday('2026-11-01') - julianday(signup_date) AS INTEGER) AS days FROM customers WHERE strftime('%m', signup_date) >= '07' ORDER BY customer_id;
