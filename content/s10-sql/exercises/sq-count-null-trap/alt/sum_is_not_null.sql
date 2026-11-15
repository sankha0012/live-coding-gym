SELECT status, COUNT(*) AS total_orders, SUM(coupon_code IS NOT NULL) AS with_coupon, SUM(actual_minutes IS NOT NULL) AS with_actual FROM orders GROUP BY status ORDER BY status;
