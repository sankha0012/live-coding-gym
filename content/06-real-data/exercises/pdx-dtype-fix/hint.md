pd.to_datetime converts the whole column, and Series.where(cond) keeps values where cond is True and puts NaN elsewhere.
