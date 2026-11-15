SELECT COUNT(DISTINCT a.customer_id) AS churned FROM orders a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
AND NOT EXISTS (SELECT 1 FROM orders b WHERE b.customer_id = a.customer_id AND b.created_at >= '2026-10-01' AND b.created_at < '2026-11-01');
