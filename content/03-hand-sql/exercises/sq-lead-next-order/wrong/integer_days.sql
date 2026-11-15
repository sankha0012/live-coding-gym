SELECT order_id, created_at,
       LEAD(created_at) OVER w AS next_created_at,
       (strftime('%s', LEAD(created_at) OVER w) - strftime('%s', created_at)) / 86400 AS days_to_next
FROM orders WHERE customer_id = 3 AND status = 'delivered'
WINDOW w AS (ORDER BY created_at, order_id) ORDER BY created_at, order_id;
