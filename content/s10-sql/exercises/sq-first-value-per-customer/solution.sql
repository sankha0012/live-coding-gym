SELECT customer_id, order_id, subtotal,
       FIRST_VALUE(subtotal) OVER w AS first_subtotal,
       ROUND(subtotal - FIRST_VALUE(subtotal) OVER w, 2) AS diff
FROM orders
WHERE customer_id IN (22, 117, 179) AND status = 'delivered' AND subtotal IS NOT NULL
WINDOW w AS (PARTITION BY customer_id ORDER BY created_at, order_id)
ORDER BY customer_id, created_at, order_id;
