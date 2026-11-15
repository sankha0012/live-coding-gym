SELECT coupon_code AS coupon, COUNT(*) AS n, 100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders) AS pct
FROM orders GROUP BY coupon_code ORDER BY n DESC;
