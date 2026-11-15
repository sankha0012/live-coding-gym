SELECT order_id, created_at,
       LEAD(created_at) OVER w AS next_created_at,
       julianday(LEAD(created_at) OVER w) - julianday(created_at) AS days_to_next
FROM orders WHERE customer_id = 3 AND status = 'delivered'
WINDOW w AS (ORDER BY created_at, order_id) ORDER BY created_at, order_id;
