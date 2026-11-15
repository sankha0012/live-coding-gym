SELECT SUM(n) AS loyal FROM (SELECT COUNT(*) AS n FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING COUNT(*) >= 3);
