SELECT order_id, customer_id, restaurant_id FROM (
  SELECT order_id, customer_id, restaurant_id,
         RANK() OVER (PARTITION BY customer_id, restaurant_id ORDER BY created_at DESC) AS rn
  FROM orders WHERE customer_id <= 5
) WHERE rn = 1 ORDER BY customer_id, restaurant_id, order_id;
