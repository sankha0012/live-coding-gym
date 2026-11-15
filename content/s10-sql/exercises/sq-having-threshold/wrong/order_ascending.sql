SELECT restaurant_id, COUNT(*) AS delivered_orders FROM orders WHERE status = 'delivered'
GROUP BY restaurant_id HAVING COUNT(*) > 100
ORDER BY delivered_orders, restaurant_id;
