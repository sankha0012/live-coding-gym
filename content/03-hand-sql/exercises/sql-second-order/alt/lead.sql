SELECT AVG(julianday(nxt) - julianday(created_at)) AS avg_days
FROM (SELECT created_at, LEAD(created_at) OVER (PARTITION BY customer_id ORDER BY created_at) AS nxt,
             ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at) AS n FROM orders WHERE status = 'delivered')
WHERE n = 1 AND nxt IS NOT NULL;
