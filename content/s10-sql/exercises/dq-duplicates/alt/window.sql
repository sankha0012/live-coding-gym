SELECT DISTINCT customer_id, restaurant_id, order_date, n FROM (
  SELECT customer_id, restaurant_id, date(created_at) AS order_date,
         COUNT(*) OVER (PARTITION BY customer_id, restaurant_id, date(created_at)) AS n
  FROM orders
)
WHERE n > 1
ORDER BY n DESC, customer_id, restaurant_id, order_date;
