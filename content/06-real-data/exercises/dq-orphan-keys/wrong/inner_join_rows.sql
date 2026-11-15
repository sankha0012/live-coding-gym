SELECT 'delivered_without_courier' AS check_name, COUNT(*) AS problem_count
FROM orders WHERE status = 'delivered' AND courier_id IS NULL
UNION ALL
SELECT 'missing_courier', COUNT(*)
FROM orders o JOIN couriers c ON c.courier_id = o.courier_id
WHERE c.courier_id IS NULL
UNION ALL
SELECT 'missing_customer', COUNT(*)
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
UNION ALL
SELECT 'missing_restaurant', COUNT(*)
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.restaurant_id IS NULL
ORDER BY check_name;
