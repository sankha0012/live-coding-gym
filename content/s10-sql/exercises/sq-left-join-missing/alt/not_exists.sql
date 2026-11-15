SELECT customer_id, name FROM customers c
WHERE city = 'Curitiba' AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY customer_id;
