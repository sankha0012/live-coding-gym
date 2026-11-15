SELECT 'delivered_without_courier' AS check_name, SUM(status = 'delivered' AND courier_id IS NULL) AS problem_count FROM orders
UNION ALL
SELECT 'missing_courier', COUNT(*) FROM orders WHERE courier_id NOT IN (SELECT courier_id FROM couriers)
UNION ALL
SELECT 'missing_customer', COUNT(*) FROM orders WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'missing_restaurant', COUNT(*) FROM orders WHERE restaurant_id NOT IN (SELECT restaurant_id FROM restaurants)
ORDER BY check_name;
