SELECT 'delivered_without_courier' AS check_name, COUNT(*) AS problem_count
FROM orders WHERE status = 'delivered' AND courier_id IS NULL
UNION ALL
SELECT 'missing_courier', COUNT(*) FROM orders o
WHERE o.courier_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM couriers c WHERE c.courier_id = o.courier_id)
UNION ALL
SELECT 'missing_customer', COUNT(*) FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id)
UNION ALL
SELECT 'missing_restaurant', COUNT(*) FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM restaurants r WHERE r.restaurant_id = o.restaurant_id)
ORDER BY check_name;
