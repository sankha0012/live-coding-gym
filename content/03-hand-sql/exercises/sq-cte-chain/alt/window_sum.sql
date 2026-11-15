SELECT restaurant_id, city, ROUND(share, 3) AS share FROM (
  SELECT r.restaurant_id, r.city,
         SUM(o.subtotal) * 1.0 / SUM(SUM(o.subtotal)) OVER (PARTITION BY r.city) AS share
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.city, r.restaurant_id)
WHERE share > 0.2 ORDER BY city, restaurant_id;
