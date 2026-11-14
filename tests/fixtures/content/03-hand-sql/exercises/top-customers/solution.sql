SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING SUM(o.amount) > 100
ORDER BY total DESC;
