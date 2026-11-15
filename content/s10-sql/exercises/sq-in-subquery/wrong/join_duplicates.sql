SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'cancelled' AND c.customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id HAVING SUM(status = 'cancelled') >= 3)
ORDER BY c.customer_id;
