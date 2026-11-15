SELECT date(created_at) AS day, COUNT(*) AS orders,
       ROUND(AVG(COUNT(*)) OVER (ORDER BY date(created_at) ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS avg_7d
FROM orders
WHERE status = 'delivered' AND date(created_at) BETWEEN '2026-10-20' AND '2026-10-31'
GROUP BY date(created_at)
ORDER BY day;
