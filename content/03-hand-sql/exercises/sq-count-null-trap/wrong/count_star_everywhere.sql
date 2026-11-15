SELECT status, COUNT(*) AS total_orders, COUNT(*) AS with_coupon, COUNT(*) AS with_actual FROM orders GROUP BY status ORDER BY status;
