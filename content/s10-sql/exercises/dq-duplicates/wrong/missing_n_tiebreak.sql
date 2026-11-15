SELECT customer_id, restaurant_id, date(created_at) AS order_date, COUNT(*) AS n
FROM orders GROUP BY customer_id, restaurant_id, date(created_at)
HAVING COUNT(*) > 1
ORDER BY n DESC, order_date, restaurant_id, customer_id;
