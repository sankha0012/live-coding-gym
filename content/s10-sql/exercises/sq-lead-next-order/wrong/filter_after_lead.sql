SELECT order_id, created_at, next_created_at, days_to_next FROM (
  SELECT order_id, created_at, status,
         LEAD(created_at) OVER w AS next_created_at,
         ROUND(julianday(LEAD(created_at) OVER w) - julianday(created_at), 1) AS days_to_next
  FROM orders WHERE customer_id = 3
  WINDOW w AS (ORDER BY created_at, order_id)
) WHERE status = 'delivered' ORDER BY created_at, order_id;
