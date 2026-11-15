SELECT customer_id, order_id, created_at, subtotal
FROM (
  SELECT o.customer_id, o.order_id, o.created_at, o.subtotal,
         ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.created_at DESC, o.order_id DESC) AS rn
  FROM orders o JOIN customers c ON c.customer_id = o.customer_id
  WHERE c.city = 'Curitiba' AND o.status = 'delivered'
)
WHERE rn = 3
ORDER BY customer_id;
