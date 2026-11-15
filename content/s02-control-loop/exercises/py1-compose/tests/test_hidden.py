from solution import compose


def test_right_to_left():
    inc = lambda x: x + 1
    dbl = lambda x: x * 2
    assert compose(inc, dbl)(5) == 11
    assert compose(dbl, inc)(5) == 12


def test_three_functions():
    assert compose(str, abs, int)("-7") == "7"


def test_empty_is_identity():
    assert compose()(42) == 42
    assert compose()("a") == "a"


def test_single():
    assert compose(len)("abc") == 3


def test_reusable_and_args_not_mutated():
    f = compose(lambda x: x + 1, lambda x: x * 2)
    assert f(1) == 3
    assert f(1) == 3
    assert f(10) == 21
