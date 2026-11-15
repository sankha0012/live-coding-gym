WITH rev AS (SELECT r.city, o.restaurant_id, SUM(o.subtotal) AS revenue FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' GROUP BY r.city, o.restaurant_id)
SELECT a.city, a.restaurant_id, a.revenue, 1 + (SELECT COUNT(*) FROM rev b WHERE b.city = a.city AND b.revenue > a.revenue) AS rn
FROM rev a WHERE 1 + (SELECT COUNT(*) FROM rev b WHERE b.city = a.city AND b.revenue > a.revenue) <= 2 ORDER BY a.city, rn;
