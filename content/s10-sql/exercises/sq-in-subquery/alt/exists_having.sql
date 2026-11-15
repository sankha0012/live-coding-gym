SELECT c.customer_id, c.name FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'cancelled') >= 3
ORDER BY c.customer_id;
