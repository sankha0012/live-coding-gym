Count per day first, then reindex to every calendar day with fill_value=0 so gaps exist, and only then call rolling(7, min_periods=1).sum().
