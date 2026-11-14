SELECT 'missing_restaurant' AS check_name, COUNT(*) AS problem_count
FROM orders o LEFT JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.restaurant_id IS NULL
