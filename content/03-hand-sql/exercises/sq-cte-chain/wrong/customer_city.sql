WITH rev AS (
  SELECT c.city, o.restaurant_id, SUM(o.subtotal) AS revenue
  FROM orders o JOIN customers c ON c.customer_id = o.customer_id
  WHERE o.status = 'delivered' GROUP BY c.city, o.restaurant_id
),
city_total AS (SELECT city, SUM(revenue) AS total FROM rev GROUP BY city)
SELECT rev.restaurant_id, rev.city, ROUND(rev.revenue * 1.0 / ct.total, 3) AS share
FROM rev JOIN city_total ct ON ct.city = rev.city
WHERE rev.revenue * 1.0 / ct.total > 0.2
ORDER BY rev.city, rev.restaurant_id;
