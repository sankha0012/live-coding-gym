Total the spend per customer in a CTE, then NTILE(4) OVER (ORDER BY spend DESC, customer_id). Add the tie-break to the window.
