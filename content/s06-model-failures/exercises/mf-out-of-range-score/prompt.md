A model should output probabilities between 0 and 1, but a bug in a post-processing step lets some values escape. Write `clip_probs(probs: list[float]) -> tuple[list[float], int]`.

Return `(clipped, n_out_of_range)`. A value below 0 becomes 0.0 and a value above 1 becomes 1.0. A value that is exactly 0 or exactly 1 is valid and is not counted. `n_out_of_range` is the number of values that had to be changed. All inputs are finite numbers. Do not modify the input. An empty list returns `([], 0)`.
