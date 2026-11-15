SELECT status, COUNT(DISTINCT customer_id) AS n FROM orders GROUP BY status ORDER BY n DESC, status;
