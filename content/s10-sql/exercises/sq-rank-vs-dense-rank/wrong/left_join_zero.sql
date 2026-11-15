WITH c AS (
  SELECT r.restaurant_id, COUNT(o.order_id) AS orders
  FROM restaurants r LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id AND o.status = 'delivered'
  GROUP BY r.restaurant_id
)
SELECT restaurant_id, orders, RANK() OVER (ORDER BY orders DESC) AS rnk, DENSE_RANK() OVER (ORDER BY orders DESC) AS drnk FROM c ORDER BY rnk, restaurant_id;
