SELECT customer_id, spend, NTILE(4) OVER (ORDER BY spend DESC, customer_id) AS band
FROM (
  SELECT o.customer_id, ROUND(SUM(o.subtotal), 2) AS spend
  FROM orders o
  WHERE o.status = 'delivered' AND o.customer_id IN (SELECT customer_id FROM customers WHERE city = 'Curitiba')
  GROUP BY o.customer_id
)
ORDER BY band, spend DESC, customer_id;
