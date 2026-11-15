Your query passes. Now edit it by hand, without asking the assistant: keep only the cuisines with at least 18 cancelled orders. Same columns, same sort by cuisine.

Expected: 3 rows instead of 8: burger (18 cancelled), healthy (19) and pizza (22). The condition is on an aggregate, so it needs HAVING.
