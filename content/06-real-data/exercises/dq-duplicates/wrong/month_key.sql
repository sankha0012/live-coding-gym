SELECT customer_id, restaurant_id, substr(created_at, 1, 7) AS order_date, COUNT(*) AS n
FROM orders GROUP BY customer_id, restaurant_id, substr(created_at, 1, 7)
HAVING COUNT(*) > 1
ORDER BY n DESC, customer_id, restaurant_id, order_date;
