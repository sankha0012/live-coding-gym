from solution import Counter


def test_add_and_count():
    c = Counter()
    c.add("a")
    c.add("a")
    c.add("b", 5)
    assert c.count("a") == 2
    assert c.count("b") == 5
    assert c.total() == 7


def test_missing_item_is_zero():
    c = Counter()
    assert c.count("zzz") == 0
    assert c.total() == 0


def test_most_common_with_ties():
    c = Counter()
    for w in ["pear", "apple", "kiwi", "kiwi", "apple", "fig"]:
        c.add(w)
    assert c.most_common(3) == [("apple", 2), ("kiwi", 2), ("fig", 1)]


def test_most_common_edges():
    c = Counter()
    assert c.most_common(3) == []
    c.add("x")
    assert c.most_common(10) == [("x", 1)]
    assert c.most_common(0) == []


def test_instances_are_separate():
    a, b = Counter(), Counter()
    a.add("x")
    assert b.count("x") == 0


def test_reading_a_missing_item_does_not_add_it():
    c = Counter()
    c.add("a")
    assert c.count("ghost") == 0
    assert c.most_common(5) == [("a", 1)]
    assert c.total() == 1
