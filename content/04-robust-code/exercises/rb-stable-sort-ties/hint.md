sorted() is stable and accepts a tuple key. Put the None flag first, then the negated score, then the id. Negating the score gives "high first" without reverse=True.
