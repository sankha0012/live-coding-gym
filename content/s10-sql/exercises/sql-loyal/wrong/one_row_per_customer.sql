SELECT COUNT(*) AS loyal FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING COUNT(*) >= 3;
