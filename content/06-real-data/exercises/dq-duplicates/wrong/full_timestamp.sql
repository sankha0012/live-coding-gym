SELECT customer_id, restaurant_id, created_at AS order_date, COUNT(*) AS n
FROM orders GROUP BY customer_id, restaurant_id, created_at
HAVING COUNT(*) > 1
ORDER BY n DESC, customer_id, restaurant_id, order_date;
