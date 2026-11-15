Do orders with a coupon have a higher average value? `orders` has `subtotal`, `coupon_code` (empty when no coupon was used) and `status`.

Write `coupon_effect(orders)` that returns a tuple `(with_coupon, without_coupon)`: the mean `subtotal` of orders that used a coupon, and the mean of orders that did not. Both rounded to 2 decimals.

- Only orders with `status == "delivered"` count.
- An order has a coupon when `coupon_code` is not missing.
- Missing subtotals are ignored in the mean (do not turn them into 0).
- Do not modify the input dataframe.

After you code it, be ready to say whether this difference proves that coupons raise order value.
