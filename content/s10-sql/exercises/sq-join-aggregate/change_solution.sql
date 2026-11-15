SELECT r.cuisine, COUNT(*) AS orders, ROUND(SUM(o.subtotal), 2) AS revenue
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered'
GROUP BY r.cuisine
HAVING COUNT(*) >= 100
ORDER BY revenue DESC, r.cuisine;
