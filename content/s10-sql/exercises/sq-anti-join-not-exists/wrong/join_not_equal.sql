SELECT DISTINCT c.customer_id, c.name
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE c.city = 'Rio de Janeiro' AND o.status <> 'delivered'
ORDER BY c.customer_id;
