SELECT CASE WHEN subtotal < 42 THEN 'small' WHEN subtotal < 83 THEN 'medium' ELSE 'large' END AS bucket,
       COUNT(*) AS orders
FROM orders WHERE subtotal IS NOT NULL GROUP BY bucket ORDER BY bucket;
