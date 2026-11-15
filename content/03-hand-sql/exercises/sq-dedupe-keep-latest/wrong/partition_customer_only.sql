SELECT order_id, customer_id, restaurant_id FROM (
  SELECT order_id, customer_id, restaurant_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC, order_id DESC) AS rn
  FROM orders WHERE customer_id <= 5
) WHERE rn = 1 ORDER BY customer_id, restaurant_id;
