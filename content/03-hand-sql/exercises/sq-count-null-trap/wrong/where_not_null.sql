SELECT status, COUNT(*) AS total_orders, COUNT(coupon_code) AS with_coupon, COUNT(actual_minutes) AS with_actual
FROM orders WHERE actual_minutes IS NOT NULL GROUP BY status ORDER BY status;
