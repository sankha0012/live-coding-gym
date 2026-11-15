SELECT COALESCE(coupon_code, 'none') AS coupon, COUNT(*) AS n, 100.0 * COUNT(*) / SUM(COUNT(*)) OVER () AS pct
FROM orders GROUP BY 1 ORDER BY n DESC;
