SELECT status, COUNT(*) AS total_orders,
       COUNT(CASE WHEN coupon_code IS NOT NULL THEN 1 END) AS with_coupon,
       COUNT(CASE WHEN actual_minutes IS NOT NULL THEN 1 END) AS with_actual
FROM orders GROUP BY status ORDER BY status;
