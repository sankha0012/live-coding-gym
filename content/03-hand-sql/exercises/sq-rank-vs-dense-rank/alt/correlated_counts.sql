WITH c AS (SELECT restaurant_id, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY restaurant_id)
SELECT a.restaurant_id, a.orders,
       1 + (SELECT COUNT(*) FROM c b WHERE b.orders > a.orders) AS rnk,
       1 + (SELECT COUNT(DISTINCT b.orders) FROM c b WHERE b.orders > a.orders) AS drnk
FROM c a ORDER BY rnk, a.restaurant_id;
