SELECT CASE WHEN coupon_code IS NULL THEN 'none' ELSE coupon_code END AS coupon, COUNT(*) AS n,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders) AS pct
FROM orders GROUP BY 1 ORDER BY 2 DESC;
