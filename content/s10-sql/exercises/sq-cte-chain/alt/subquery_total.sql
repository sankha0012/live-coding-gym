WITH rev AS (
  SELECT r.city, o.restaurant_id, SUM(o.subtotal) AS revenue
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.city, o.restaurant_id
)
SELECT a.restaurant_id, a.city,
       ROUND(a.revenue / (SELECT SUM(b.revenue) FROM rev b WHERE b.city = a.city), 3) AS share
FROM rev a
WHERE a.revenue / (SELECT SUM(b.revenue) FROM rev b WHERE b.city = a.city) > 0.2
ORDER BY a.city, a.restaurant_id;
