SELECT restaurant_id, orders,
       RANK() OVER w AS rnk, DENSE_RANK() OVER w AS drnk
FROM (SELECT restaurant_id, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY restaurant_id)
WINDOW w AS (ORDER BY orders DESC)
ORDER BY rnk, restaurant_id;
