SELECT COUNT(*) AS loyal FROM (SELECT customer_id FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING COUNT(DISTINCT restaurant_id) >= 3);
