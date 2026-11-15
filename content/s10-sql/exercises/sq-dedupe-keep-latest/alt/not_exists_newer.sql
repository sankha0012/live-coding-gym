SELECT o.order_id, o.customer_id, o.restaurant_id FROM orders o
WHERE o.customer_id <= 5
  AND NOT EXISTS (
    SELECT 1 FROM orders x
    WHERE x.customer_id = o.customer_id AND x.restaurant_id = o.restaurant_id
      AND (x.created_at > o.created_at OR (x.created_at = o.created_at AND x.order_id > o.order_id)))
ORDER BY o.customer_id, o.restaurant_id;
