SELECT r.city, o.restaurant_id, SUM(o.subtotal) AS revenue, 1 AS rn FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' GROUP BY r.city, o.restaurant_id ORDER BY revenue DESC LIMIT 2;
