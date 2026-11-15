from solution import set_diff_report


def test_basic():
    assert set_diff_report(["a", "b"], ["b", "c"]) == {"added": ["c"], "removed": ["a"], "kept": ["b"]}


def test_sorted_and_deduplicated():
    got = set_diff_report(["z", "y", "y", "k"], ["k", "k", "x", "w"])
    assert got == {"added": ["w", "x"], "removed": ["y", "z"], "kept": ["k"]}


def test_identical():
    assert set_diff_report(["a", "b"], ["b", "a"]) == {"added": [], "removed": [], "kept": ["a", "b"]}


def test_empty():
    assert set_diff_report([], []) == {"added": [], "removed": [], "kept": []}
    assert set_diff_report([], ["a"]) == {"added": ["a"], "removed": [], "kept": []}


def test_many_items_come_back_sorted():
    old = ["h", "d", "b", "f", "j", "l", "n", "p"]
    new = ["q", "o", "m", "k", "i", "g", "e", "c", "b", "d"]
    assert set_diff_report(old, new) == {
        "added": ["c", "e", "g", "i", "k", "m", "o", "q"],
        "removed": ["f", "h", "j", "l", "n", "p"],
        "kept": ["b", "d"],
    }


def test_duplicates_removed_in_every_list():
    got = set_diff_report(["k", "k", "a", "a", "z"], ["k", "b", "b", "q"])
    assert got == {"added": ["b", "q"], "removed": ["a", "z"], "kept": ["k"]}
    got = set_diff_report([], ["c", "c", "c"])
    assert got == {"added": ["c"], "removed": [], "kept": []}
    got = set_diff_report(["c", "c"], [])
    assert got == {"added": [], "removed": ["c"], "kept": []}
