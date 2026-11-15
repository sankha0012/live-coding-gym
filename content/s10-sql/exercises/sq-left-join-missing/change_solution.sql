SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE c.city = 'Sao Paulo' AND o.order_id IS NULL
ORDER BY c.customer_id;
