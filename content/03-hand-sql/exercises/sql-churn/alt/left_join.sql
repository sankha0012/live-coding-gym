SELECT COUNT(*) AS churned FROM (SELECT DISTINCT customer_id FROM orders WHERE strftime('%Y-%m', created_at) = '2026-08') a
LEFT JOIN (SELECT DISTINCT customer_id FROM orders WHERE strftime('%Y-%m', created_at) = '2026-10') b ON b.customer_id = a.customer_id WHERE b.customer_id IS NULL;
