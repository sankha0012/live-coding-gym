SELECT order_id, created_at,
       LAG(created_at) OVER w AS next_created_at,
       ROUND(julianday(created_at) - julianday(LAG(created_at) OVER w), 1) AS days_to_next
FROM orders WHERE customer_id = 3 AND status = 'delivered'
WINDOW w AS (ORDER BY created_at, order_id) ORDER BY created_at, order_id;
