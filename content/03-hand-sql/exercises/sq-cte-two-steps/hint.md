Step one is a CTE with GROUP BY restaurant_id and ROUND(SUM(...), 2). Step two selects from the CTE and compares revenue with a scalar subquery that averages the same CTE.
