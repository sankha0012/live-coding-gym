WITH m AS (
  SELECT r.city, strftime('%Y-%m', o.created_at) AS month, SUM(o.subtotal) AS revenue
  FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
  WHERE o.status = 'delivered' GROUP BY r.city, strftime('%Y-%m', o.created_at)
)
SELECT a.city, a.month, ROUND(a.revenue, 2) AS revenue,
       ROUND(100.0 * (a.revenue - p.revenue) / p.revenue, 1) AS growth_pct
FROM m a
LEFT JOIN m p ON p.city = a.city AND p.month = strftime('%Y-%m', a.month || '-01', '-1 month')
ORDER BY a.city, a.month;
