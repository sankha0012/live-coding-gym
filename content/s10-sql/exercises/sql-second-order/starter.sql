WITH ranked AS (
  SELECT customer_id, created_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at) AS n
  FROM orders
  WHERE status = 'delivered'
)
SELECT ...
