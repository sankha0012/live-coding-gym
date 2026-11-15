Your query passes. Now edit it by hand, without asking the assistant: keep the oldest order for each (customer_id, restaurant_id) pair instead of the latest. Oldest means the lowest created_at; on a tie the lower order_id wins. Same columns, same sort.

Expected: still 66 rows, but many are different orders. For customer 1 and restaurant 2 you now get order 100046 instead of 900002. Both ORDER BY directions inside the window must flip.
