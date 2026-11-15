SELECT 'by_courier' AS check_name,
       (SELECT COUNT(*) FROM orders) AS total_orders
