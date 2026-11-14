Subtracting two datetimes gives a timedelta. Use `total_seconds()`, not `.days`, which throws away the fraction.
