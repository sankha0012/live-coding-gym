SELECT status, COUNT(*) AS total_orders, COUNT(NULLIF(coupon_code, '')) AS with_coupon, COUNT(actual_minutes) AS with_actual FROM orders GROUP BY status ORDER BY status;
