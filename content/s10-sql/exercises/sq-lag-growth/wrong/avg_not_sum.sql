WITH m AS (
  SELECT r.city, strftime('%Y-%m', o.created_at) AS month, AVG(o.subtotal) AS revenue
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.city, strftime('%Y-%m', o.created_at)
)
SELECT city, month, ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS growth_pct
FROM m WINDOW w AS (PARTITION BY city ORDER BY month) ORDER BY city, month;
