Any arithmetic with NULL gives NULL, so wrap subtotal in COALESCE(subtotal, 0). Filter the NULLs with IS NULL, not = NULL.
