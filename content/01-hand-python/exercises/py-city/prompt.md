Orders are dicts with 'city', 'status', 'subtotal' (may be None) and 'fee'. Return {city: GMV} for delivered orders only, GMV = subtotal + fee, None counts as 0, rounded to 2 decimals.

*Group-by in plain Python.*
