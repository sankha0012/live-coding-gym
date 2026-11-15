SELECT MAX(o.order_id) AS order_id, o.customer_id, o.restaurant_id
FROM orders o JOIN (SELECT customer_id, restaurant_id, MAX(created_at) AS m FROM orders WHERE customer_id <= 5 GROUP BY customer_id, restaurant_id) t
  ON t.customer_id = o.customer_id AND t.restaurant_id = o.restaurant_id AND t.m = o.created_at
GROUP BY o.customer_id, o.restaurant_id ORDER BY o.customer_id, o.restaurant_id;
