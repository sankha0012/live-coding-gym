## Contract

`merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame`

Both frames have a `restaurant_id` column. `restaurants` carries extra columns such as `city`.

- The result is a left merge of `orders` with `restaurants` on `restaurant_id`: every order keeps its row and gains the restaurant columns.
- An order whose `restaurant_id` is not in `restaurants` stays in the result with NaN in the restaurant columns.
- Row order is the order of `orders`.
- The result must have exactly `len(orders)` rows. If it does not, raise `ValueError`. Nothing partial is returned.
- A duplicated `restaurant_id` in `restaurants` is an error only if it changes the row count. A duplicate key that no order uses is not an error.
- Neither input is modified, including when the error is raised. An empty `orders` returns an empty frame.

Example: orders with `restaurant_id` 1, 99, 2 and restaurants 1 and 2 give three rows, with NaN `city` in the middle one.

## Library notes

- `DataFrame.merge(right, on=, how="left", validate=None)` returns a new frame. A left merge keeps the order of the left frame, and a duplicated right key produces one output row per match.
- `validate="m:1"` raises `pandas.errors.MergeError`, a subclass of `ValueError`, when the right keys are not unique. It looks at all right rows, whether or not an order uses them.
- `DataFrame.duplicated(subset=None, keep="first")` returns a boolean Series marking repeated rows.

## Gotchas

- A join that silently multiplies rows inflates revenue and order counts downstream. Check cardinality right after every join.
- Count checks beat eyeballing: a changed row count is cheap to detect, a few wrong values are not.
- Do not repair the data in a join helper (for example by dropping duplicates). Fail loudly and let the owner of the data fix it.
