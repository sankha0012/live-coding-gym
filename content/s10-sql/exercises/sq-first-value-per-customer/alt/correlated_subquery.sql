SELECT o.customer_id, o.order_id, o.subtotal,
       (SELECT f.subtotal FROM orders f
         WHERE f.customer_id = o.customer_id AND f.status = 'delivered' AND f.subtotal IS NOT NULL
         ORDER BY f.created_at, f.order_id LIMIT 1) AS first_subtotal,
       ROUND(o.subtotal - (SELECT f.subtotal FROM orders f
         WHERE f.customer_id = o.customer_id AND f.status = 'delivered' AND f.subtotal IS NOT NULL
         ORDER BY f.created_at, f.order_id LIMIT 1), 2) AS diff
FROM orders o
WHERE o.customer_id IN (22, 117, 179) AND o.status = 'delivered' AND o.subtotal IS NOT NULL
ORDER BY o.customer_id, o.created_at, o.order_id;
