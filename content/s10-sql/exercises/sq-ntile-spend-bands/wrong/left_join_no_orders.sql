WITH s AS (
  SELECT c.customer_id, ROUND(COALESCE(SUM(o.subtotal), 0), 2) AS spend
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'delivered'
  WHERE c.city = 'Curitiba'
  GROUP BY c.customer_id
)
SELECT customer_id, spend, NTILE(4) OVER (ORDER BY spend DESC, customer_id) AS band
FROM s ORDER BY band, spend DESC, customer_id;
