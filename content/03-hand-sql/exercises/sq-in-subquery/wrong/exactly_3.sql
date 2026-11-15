SELECT customer_id, name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'cancelled' GROUP BY customer_id HAVING COUNT(*) = 3)
ORDER BY customer_id;
