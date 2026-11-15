WITH c AS (SELECT restaurant_id, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY restaurant_id)
SELECT restaurant_id, orders, ROW_NUMBER() OVER (ORDER BY orders DESC, restaurant_id) AS rnk, DENSE_RANK() OVER (ORDER BY orders DESC) AS drnk FROM c ORDER BY rnk, restaurant_id;
