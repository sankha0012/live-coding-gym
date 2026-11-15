SELECT customer_id, name FROM customers
WHERE city = 'Curitiba' AND customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY customer_id;
