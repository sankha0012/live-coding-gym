SELECT r.city,
       COUNT(*) AS orders
       -- cancellation rate?
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city;
