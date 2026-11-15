SELECT restaurant_id, COUNT(*) AS delivered_orders FROM orders
GROUP BY restaurant_id HAVING COUNT(*) > 100
ORDER BY delivered_orders DESC, restaurant_id;
