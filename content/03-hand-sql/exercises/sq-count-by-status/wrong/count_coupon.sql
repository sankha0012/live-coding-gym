SELECT status, COUNT(coupon_code) AS n FROM orders GROUP BY status ORDER BY n DESC, status;
