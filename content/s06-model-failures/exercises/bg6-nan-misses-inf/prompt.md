A model sometimes returns `NaN`, `inf`, `-inf` or `None` instead of a score. Write `guard_scores(scores: list, fallback: float = 0.5) -> tuple[list[float], int]`.

Replace every bad score with `fallback` and return `(clean_scores, bad_count)`. A score is bad when it is `None`, NaN, positive or negative infinity, or not a number at all (for example a string). A bool is not a score either, so `True` and `False` are bad. Good scores keep their value and their position. Do not modify the input list. An empty list returns `([], 0)`.


An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
