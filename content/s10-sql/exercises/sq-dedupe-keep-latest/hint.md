ROW_NUMBER() OVER (PARTITION BY the pair ORDER BY created_at DESC, order_id DESC), then keep rn = 1 in an outer query.
