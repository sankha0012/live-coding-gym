from solution import clip_probs


def test_in_range_untouched():
    assert clip_probs([0.0, 0.4, 1.0]) == ([0.0, 0.4, 1.0], 0)


def test_clips_and_counts():
    got, n = clip_probs([-0.2, 0.5, 1.7, 3])
    assert got == [0.0, 0.5, 1.0, 1.0]
    assert n == 3


def test_boundaries_not_counted():
    assert clip_probs([0, 1, 1.0000001])[1] == 1


def test_empty():
    assert clip_probs([]) == ([], 0)


def test_input_not_modified():
    src = [2.0, -1.0]
    clip_probs(src)
    assert src == [2.0, -1.0]
