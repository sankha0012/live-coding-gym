WITH rev AS (
  SELECT r.city, o.restaurant_id, SUM(o.subtotal) AS revenue
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.city, o.restaurant_id
)
SELECT restaurant_id, city, ROUND(revenue * 1.0 / (SELECT SUM(revenue) FROM rev), 3) AS share
FROM rev WHERE revenue * 1.0 / (SELECT SUM(revenue) FROM rev) > 0.2
ORDER BY city, restaurant_id;
