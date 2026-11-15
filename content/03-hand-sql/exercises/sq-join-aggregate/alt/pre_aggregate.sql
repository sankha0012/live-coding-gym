SELECT r.cuisine, SUM(t.n) AS orders, ROUND(SUM(t.s), 2) AS revenue
FROM (SELECT restaurant_id, COUNT(*) AS n, SUM(subtotal) AS s FROM orders WHERE status = 'delivered' GROUP BY restaurant_id) t
JOIN restaurants r ON r.restaurant_id = t.restaurant_id
GROUP BY r.cuisine ORDER BY revenue DESC, r.cuisine;
