WITH a AS (SELECT AVG(subtotal) AS m FROM orders WHERE status = 'delivered')
SELECT o.order_id, o.subtotal FROM orders o, a
WHERE o.status = 'delivered' AND o.subtotal > 2 * a.m ORDER BY o.order_id;
