The filter `v != float("nan")` is always true because NaN is never equal to anything, so NaN values are never removed and the mean comes out as NaN instead of the mean of the valid numbers.
