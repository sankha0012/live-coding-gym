SELECT COUNT(DISTINCT a.customer_id) AS churned FROM orders a JOIN orders b ON a.customer_id <> b.customer_id
WHERE strftime('%Y-%m', a.created_at) = '2026-08' AND strftime('%Y-%m', b.created_at) = '2026-10';
