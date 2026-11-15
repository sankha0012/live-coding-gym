SELECT customer_id, CAST(julianday('2026-11-01') - julianday(signup_date) AS INTEGER) AS days FROM customers WHERE julianday(signup_date) >= julianday('2026-07-01') ORDER BY customer_id;
