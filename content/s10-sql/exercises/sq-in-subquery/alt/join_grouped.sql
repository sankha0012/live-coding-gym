SELECT c.customer_id, c.name FROM customers c
JOIN (SELECT customer_id, COUNT(*) AS n FROM orders WHERE status = 'cancelled' GROUP BY customer_id) x ON x.customer_id = c.customer_id
WHERE x.n >= 3
ORDER BY c.customer_id;
