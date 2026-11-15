WITH s AS (
  SELECT c.customer_id, ROUND(SUM(o.subtotal), 2) AS spend
  FROM customers c JOIN orders o ON o.customer_id = c.customer_id
  WHERE c.city = 'Curitiba' AND o.status = 'delivered'
  GROUP BY c.customer_id
), r AS (
  SELECT customer_id, spend, ROW_NUMBER() OVER (ORDER BY spend DESC, customer_id) - 1 AS i, COUNT(*) OVER () AS n FROM s
)
SELECT customer_id, spend,
       1 + (i * 4 / n) AS band
FROM r ORDER BY band, spend DESC, customer_id;
