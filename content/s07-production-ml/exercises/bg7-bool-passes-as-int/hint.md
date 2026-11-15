Pass `True` for an `int` field and `float("nan")` for a float field with no bounds. Does the code report a violation? Ask yourself what `isinstance(True, int)` and `float("nan") < 0` return.
