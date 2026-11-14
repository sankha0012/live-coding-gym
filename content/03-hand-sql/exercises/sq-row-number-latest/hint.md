ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC, order_id DESC) in a subquery, then keep the row you want outside. Which rn is the second most recent?
