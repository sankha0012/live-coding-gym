SELECT status, COUNT(*) AS n FROM orders WHERE status = 'delivered' GROUP BY status ORDER BY n DESC, status;
