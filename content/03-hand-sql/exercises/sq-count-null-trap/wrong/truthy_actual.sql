SELECT status, COUNT(*) AS total_orders, COUNT(coupon_code) AS with_coupon, SUM(actual_minutes > 0) AS with_actual FROM orders GROUP BY status ORDER BY status;
