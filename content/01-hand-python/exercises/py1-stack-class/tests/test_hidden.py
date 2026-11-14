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
