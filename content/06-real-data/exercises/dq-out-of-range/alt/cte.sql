WITH f AS (
  SELECT CASE WHEN actual_minutes > 4 * promised_minutes THEN 1 ELSE 0 END AS a,
         CASE WHEN subtotal < 0 OR delivery_fee < 0 THEN 1 ELSE 0 END AS b,
         CASE WHEN promised_minutes <= 0 OR actual_minutes < 0 THEN 1 ELSE 0 END AS c,
         CASE WHEN subtotal > 150 THEN 1 ELSE 0 END AS d
  FROM orders
)
SELECT 'actual_over_4x' AS rule_name, SUM(a) AS violations FROM f
UNION ALL SELECT 'negative_amount', SUM(b) FROM f
UNION ALL SELECT 'nonpositive_minutes', SUM(c) FROM f
UNION ALL SELECT 'subtotal_over_150', SUM(d) FROM f
ORDER BY rule_name;
