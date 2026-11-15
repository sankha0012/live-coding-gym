The bare `except:` returns 0 for any failure, so bad input such as "abc" or "3.5" is silently turned into a quantity of 0 instead of raising ValueError.
