`orders` has `restaurant_id`. `restaurants` has `restaurant_id`, `city` and `cuisine`.

Write `city_cuisine_counts(orders, restaurants)` that returns a DataFrame with one row per city, one column per cuisine, and the number of orders in each cell.

- Every order counts, whatever its status. Every `restaurant_id` in `orders` exists in `restaurants`.
- The index is `city` and the columns are `cuisine`. Both are sorted alphabetically.
- A city and cuisine pair with no orders shows `0`, not a missing value. Cells are integers.
- Only cities and cuisines that have at least one order appear.
- Do not modify the input dataframes.
