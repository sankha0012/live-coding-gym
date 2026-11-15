SELECT o.order_id, o.created_at,
       (SELECT n.created_at FROM orders n WHERE n.customer_id = 3 AND n.status = 'delivered'
          AND (n.created_at > o.created_at OR (n.created_at = o.created_at AND n.order_id > o.order_id))
        ORDER BY n.created_at, n.order_id LIMIT 1) AS next_created_at,
       ROUND(julianday((SELECT n.created_at FROM orders n WHERE n.customer_id = 3 AND n.status = 'delivered'
          AND (n.created_at > o.created_at OR (n.created_at = o.created_at AND n.order_id > o.order_id))
        ORDER BY n.created_at, n.order_id LIMIT 1)) - julianday(o.created_at), 1) AS days_to_next
FROM orders o WHERE o.customer_id = 3 AND o.status = 'delivered'
ORDER BY o.created_at, o.order_id;
