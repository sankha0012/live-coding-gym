SELECT COALESCE(coupon_code, 'none') AS coupon, COUNT(coupon_code) AS n, 100.0 * COUNT(coupon_code) / (SELECT COUNT(*) FROM orders) AS pct
FROM orders GROUP BY coupon ORDER BY n DESC;
