SELECT order_id, created_at, next_created_at, days_to_next FROM (
  SELECT order_id, customer_id, created_at,
         LEAD(created_at) OVER w AS next_created_at,
         ROUND(julianday(LEAD(created_at) OVER w) - julianday(created_at), 1) AS days_to_next
  FROM orders WHERE status = 'delivered'
  WINDOW w AS (ORDER BY created_at, order_id)
) WHERE customer_id = 3 ORDER BY created_at, order_id;
