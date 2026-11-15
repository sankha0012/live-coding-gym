SELECT cuisine, ROUND(AVG(a), 2) AS avg_subtotal FROM (
  SELECT r.cuisine, r.restaurant_id, AVG(o.subtotal) AS a
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.cuisine, r.restaurant_id)
GROUP BY cuisine ORDER BY cuisine;
