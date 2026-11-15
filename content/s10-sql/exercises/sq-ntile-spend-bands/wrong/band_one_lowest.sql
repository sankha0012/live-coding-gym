WITH s AS (
  SELECT c.customer_id, ROUND(SUM(o.subtotal), 2) AS spend
  FROM customers c JOIN orders o ON o.customer_id = c.customer_id
  WHERE c.city = 'Curitiba' AND o.status = 'delivered'
  GROUP BY c.customer_id
)
SELECT customer_id, spend, NTILE(4) OVER (ORDER BY spend, customer_id) AS band
FROM s ORDER BY band, spend DESC, customer_id;
