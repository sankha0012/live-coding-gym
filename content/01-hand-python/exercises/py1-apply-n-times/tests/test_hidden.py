from solution import apply_n_times


def test_double():
    assert apply_n_times(lambda v: v * 2, 3, 1) == 8


def test_zero_returns_input_without_calls():
    calls = []
    assert apply_n_times(lambda v: calls.append(v) or v, 0, "x") == "x"
    assert calls == []


def test_call_count():
    calls = []

    def f(v):
        calls.append(v)
        return v + 1

    assert apply_n_times(f, 4, 10) == 14
    assert calls == [10, 11, 12, 13]


def test_strings():
    assert apply_n_times(lambda s: s + "!", 2, "hi") == "hi!!"
