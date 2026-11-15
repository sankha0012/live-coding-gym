Write `build_preprocessor(numeric: list[str], categorical: list[str]) -> ColumnTransformer` for a pandas DataFrame.

- The numeric columns go through `StandardScaler`.
- The categorical columns go through `OneHotEncoder` with `handle_unknown="ignore"` and `sparse_output=False`.
- The transformers come in that order, so the output has the scaled numeric columns first, then the one-hot columns. Any other column in the frame is dropped.
- Do not fit it inside the function; return it unfitted.

A category that was not seen in training must give a row of zeros for that column's one-hot block, not an error. An empty `numeric` or `categorical` list must work.
