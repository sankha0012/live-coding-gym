SELECT COALESCE(coupon_code, 'none') AS coupon, COUNT(*) AS n, 100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders) AS pct
FROM orders GROUP BY coupon ORDER BY n DESC;