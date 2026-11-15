SELECT customer_id, (strftime('%m', '2026-11-01') - strftime('%m', signup_date)) * 30 AS days FROM customers WHERE signup_date >= '2026-07-01' ORDER BY customer_id;
