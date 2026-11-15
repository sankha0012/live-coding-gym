SELECT CASE WHEN subtotal IS NULL THEN 'unknown' WHEN subtotal < 42 THEN 'small' WHEN subtotal <= 83 THEN 'medium' ELSE 'large' END AS bucket,
       COUNT(*) AS orders
FROM orders GROUP BY bucket ORDER BY bucket;
