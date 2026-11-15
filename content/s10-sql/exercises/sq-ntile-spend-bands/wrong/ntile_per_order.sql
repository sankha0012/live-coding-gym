SELECT c.customer_id, o.subtotal AS spend, NTILE(4) OVER (ORDER BY o.subtotal DESC, c.customer_id) AS band
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE c.city = 'Curitiba' AND o.status = 'delivered'
ORDER BY band, spend DESC, customer_id;
