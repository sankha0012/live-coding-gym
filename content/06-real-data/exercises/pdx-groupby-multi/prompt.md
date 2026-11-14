Write `city_cuisine_summary(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame`.

Join each order with its restaurant (`restaurant_id`), then group by `city` and `cuisine`. Return a frame with exactly these columns, in this order:

- `city`
- `cuisine`
- `orders`: the number of orders in the group (every order counts, even if its subtotal is missing).
- `avg_subtotal`: the mean `subtotal` of the group, ignoring missing values, rounded to 2 decimals.

Sort by `orders` descending, then `city` ascending, then `cuisine` ascending. The index is `0, 1, 2, ...`. Orders whose restaurant is not in `restaurants` are ignored.
