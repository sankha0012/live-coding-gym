You need the most recent order of each customer, with all of its columns, to feed a customer table. You wrote it with `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC, order_id DESC)` and kept `rn = 1`. The interviewer asks: "Why not simply `GROUP BY customer_id` with `MAX(created_at)`? It is shorter."

Explain when each one is the right tool, what goes wrong with the GROUP BY version for this task, and how you handle two orders with the same timestamp.
