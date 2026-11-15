SELECT 'by_courier' AS check_name, (SELECT COUNT(DISTINCT customer_id) FROM orders) AS total_orders, SUM(n) AS grouped_total, (SELECT COUNT(DISTINCT customer_id) FROM orders) - SUM(n) AS difference
FROM (SELECT COUNT(*) AS n FROM orders o JOIN couriers c ON c.courier_id = o.courier_id GROUP BY c.courier_id)
UNION ALL
SELECT 'by_restaurant', (SELECT COUNT(DISTINCT customer_id) FROM orders), SUM(n), (SELECT COUNT(DISTINCT customer_id) FROM orders) - SUM(n)
FROM (SELECT COUNT(*) AS n FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.restaurant_id)
UNION ALL
SELECT 'by_status', (SELECT COUNT(DISTINCT customer_id) FROM orders), SUM(n), (SELECT COUNT(DISTINCT customer_id) FROM orders) - SUM(n)
FROM (SELECT COUNT(*) AS n FROM orders GROUP BY status)
ORDER BY check_name;
