The inner query returns one column of customer ids: filter cancelled orders, GROUP BY customer, then HAVING COUNT(*) >= 3.
