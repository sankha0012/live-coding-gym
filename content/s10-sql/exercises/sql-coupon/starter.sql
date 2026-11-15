SELECT COALESCE(coupon_code, 'none') AS coupon, COUNT(*) AS n
FROM orders
GROUP BY coupon;
