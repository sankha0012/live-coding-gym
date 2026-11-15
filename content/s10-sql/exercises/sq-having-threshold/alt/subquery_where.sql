SELECT restaurant_id, delivered_orders FROM (
  SELECT restaurant_id, COUNT(*) AS delivered_orders FROM orders WHERE status = 'delivered' GROUP BY restaurant_id
) WHERE delivered_orders > 100
ORDER BY delivered_orders DESC, restaurant_id;
