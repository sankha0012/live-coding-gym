WITH s AS (
  SELECT c.customer_id, ROUND(SUM(o.subtotal), 2) AS spend
  FROM customers c JOIN orders o ON o.customer_id = c.customer_id
  WHERE c.city = 'Curitiba' AND o.status = 'delivered'
  GROUP BY c.customer_id
)
SELECT customer_id, spend, MIN(4, 1 + (ROW_NUMBER() OVER (ORDER BY spend DESC, customer_id) - 1) / 8) AS band
FROM s ORDER BY band, spend DESC, customer_id;
