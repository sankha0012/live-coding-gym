SELECT customer_id, name FROM customers WHERE city = 'Curitiba'
EXCEPT
SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id
ORDER BY 1;
