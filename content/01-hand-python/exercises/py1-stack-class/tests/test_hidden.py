import pytest

from solution import Stack


def test_lifo():
    s = Stack()
    for x in [1, 2, 3]:
        s.push(x)
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]


def test_peek_does_not_remove():
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b"
    assert len(s) == 2


def test_len_tracks_pushes_and_pops():
    s = Stack()
    assert len(s) == 0
    s.push(1)
    s.push(2)
    s.pop()
    assert len(s) == 1


def test_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()
    s.push(1)
    s.pop()
    with pytest.raises(IndexError):
        s.pop()


def test_falsy_items_are_ordinary_items():
    s = Stack()
    for x in [0, "", None, [], False]:
        s.push(x)
    assert len(s) == 5
    assert s.peek() is False
    assert [s.pop() for _ in range(5)] == [False, [], None, "", 0]
    assert len(s) == 0
    with pytest.raises(IndexError):
        s.pop()


def test_stacks_are_independent():
    a, b = Stack(), Stack()
    a.push(1)
    assert len(b) == 0
    with pytest.raises(IndexError):
        b.pop()
    assert a.pop() == 1
