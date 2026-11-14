Some orders have an empty `subtotal` (NaN in pandas). Write `fill_subtotal(orders: pd.DataFrame) -> pd.DataFrame`.

It returns a copy of `orders` where every missing `subtotal` is replaced by the median `subtotal` of the same `restaurant_id`. The median ignores missing values. If a restaurant has no known subtotal at all, use the median of the whole `subtotal` column instead.

Rules:

- Known subtotals and all other columns stay unchanged.
- The rows keep their order and their index.
- Do not modify the input frame.
- An empty frame, or a frame with nothing missing, comes back unchanged.
