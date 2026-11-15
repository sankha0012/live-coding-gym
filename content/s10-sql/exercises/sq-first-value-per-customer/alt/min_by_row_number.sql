WITH t AS (
  SELECT customer_id, order_id, created_at, subtotal,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at, order_id) AS rn
  FROM orders
  WHERE customer_id IN (22, 117, 179) AND status = 'delivered' AND subtotal IS NOT NULL
)
SELECT t.customer_id, t.order_id, t.subtotal, f.subtotal AS first_subtotal,
       ROUND(t.subtotal - f.subtotal, 2) AS diff
FROM t JOIN t f ON f.customer_id = t.customer_id AND f.rn = 1
ORDER BY t.customer_id, t.created_at, t.order_id;
