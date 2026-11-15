Add an optional second parameter `add_flag`, default `False`. When it is `True`, the returned frame also gets a new last column `subtotal_was_missing` (booleans) that is `True` for the rows whose `subtotal` was missing in the input and `False` for all others. The filling itself is the same. With the default, no column is added and nothing changes.

Example: subtotals `10, NaN, 30` give `subtotal_was_missing` equal to `False, True, False`.
