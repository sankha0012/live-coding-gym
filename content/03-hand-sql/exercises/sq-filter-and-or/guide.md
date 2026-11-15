**Why this matters.** Mixing AND and OR is where logic bugs hide. SQL does not read left to right: AND binds tighter than OR, so a missing bracket changes the meaning without any error.

**How we get there.**
1. Start with the simple conditions that must all hold: `status = 'delivered'` and `subtotal > 140`.
2. Now the either-or part: used a coupon, or had free delivery. Coupon means `coupon_code IS NOT NULL`, because comparing NULL with `=` or `!=` never matches.
3. Free delivery means `delivery_fee = 0`.
4. Join these two with OR, and put them in parentheses: `(coupon_code IS NOT NULL OR delivery_fee = 0)`.
5. Join that group to the other conditions with AND, and select `order_id, subtotal`.

**Check it.** Rows with a NULL subtotal fail `subtotal > 140`, so they drop out. It is one pass, linear.

**Watch out.** Without the parentheses, AND groups first, so `delivery_fee = 0` stands alone and any cancelled or cheap order with free delivery slips through (357 rows instead of 28).
