SELECT bucket, COUNT(*) AS orders FROM (
  SELECT CASE WHEN subtotal IS NULL THEN 'unknown' WHEN subtotal >= 83 THEN 'large' WHEN subtotal >= 42 THEN 'medium' ELSE 'small' END AS bucket
  FROM orders)
GROUP BY bucket ORDER BY bucket;
