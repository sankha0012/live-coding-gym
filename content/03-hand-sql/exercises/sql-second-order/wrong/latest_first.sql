WITH ranked AS (SELECT customer_id, created_at, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS n FROM orders WHERE status = 'delivered')
SELECT AVG(julianday(a.created_at) - julianday(b.created_at)) AS avg_days FROM ranked a JOIN ranked b ON a.customer_id = b.customer_id AND a.n = 1 AND b.n = 2;
