WITH d AS (
  SELECT o.* FROM orders o WHERE o.status = 'delivered' AND o.customer_id IN (SELECT customer_id FROM customers WHERE city = 'Curitiba')
)
SELECT customer_id,
       (SELECT order_id FROM d x WHERE x.customer_id = k.customer_id ORDER BY created_at DESC, order_id DESC LIMIT 1 OFFSET 1) AS order_id,
       (SELECT created_at FROM d x WHERE x.customer_id = k.customer_id ORDER BY created_at DESC, order_id DESC LIMIT 1 OFFSET 1) AS created_at,
       (SELECT subtotal FROM d x WHERE x.customer_id = k.customer_id ORDER BY created_at DESC, order_id DESC LIMIT 1 OFFSET 1) AS subtotal
FROM (SELECT customer_id FROM d GROUP BY customer_id HAVING COUNT(*) >= 2) k
ORDER BY customer_id;
