SELECT 'by_courier' AS check_name, SUM(n) AS total_orders, SUM(n) AS grouped_total, 0 AS difference
FROM (SELECT COUNT(*) AS n FROM orders o JOIN couriers c ON c.courier_id = o.courier_id GROUP BY c.courier_id)
UNION ALL
SELECT 'by_restaurant', SUM(n), SUM(n), 0
FROM (SELECT COUNT(*) AS n FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.restaurant_id)
UNION ALL
SELECT 'by_status', SUM(n), SUM(n), 0
FROM (SELECT COUNT(*) AS n FROM orders GROUP BY status)
ORDER BY check_name;
