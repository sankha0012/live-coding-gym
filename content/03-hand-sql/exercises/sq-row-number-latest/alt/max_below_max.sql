SELECT o.customer_id, o.order_id, o.created_at, o.subtotal
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
WHERE c.city = 'Curitiba' AND o.status = 'delivered'
  AND (SELECT COUNT(*) FROM orders p
       WHERE p.customer_id = o.customer_id AND p.status = 'delivered'
         AND (p.created_at > o.created_at OR (p.created_at = o.created_at AND p.order_id > o.order_id))) = 1
ORDER BY o.customer_id;
