A frame was loaded with every column as text (`dtype=str`, empty cells kept as empty strings). Write `fix_types(raw: pd.DataFrame) -> pd.DataFrame`.

It returns a copy where:

- `created_at` is a datetime column.
- `coupon_code` is NaN when the text is empty or only spaces. Other coupon codes stay as they are.
- `order_id`, `customer_id` and `restaurant_id` are integers (`int64`).
- `courier_id` can be empty (no courier assigned). Make it the nullable integer type `Int64`, with empty text becoming `<NA>`.

All other columns stay unchanged. Do not modify the input frame. The frame can have zero rows.
