SELECT CASE WHEN coupon_code = NULL THEN 'none' ELSE coupon_code END AS coupon, COUNT(*) AS n, 100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders) AS pct
FROM orders GROUP BY coupon ORDER BY n DESC;
