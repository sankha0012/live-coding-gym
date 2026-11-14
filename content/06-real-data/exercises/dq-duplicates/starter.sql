SELECT customer_id, restaurant_id, date(created_at) AS order_date, COUNT(*) AS n
FROM orders
