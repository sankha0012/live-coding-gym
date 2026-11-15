SELECT c.customer_id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.order_id IS NULL
WHERE c.city = 'Curitiba' ORDER BY c.customer_id;
