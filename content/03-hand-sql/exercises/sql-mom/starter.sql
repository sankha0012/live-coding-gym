WITH m AS (
  SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS orders
  FROM orders
  WHERE status = 'delivered'
  GROUP BY month
)
SELECT ...
