SELECT s.status, (SELECT COUNT(*) FROM orders o WHERE o.status = s.status) AS n
FROM (SELECT DISTINCT status FROM orders) s ORDER BY n DESC, s.status;
