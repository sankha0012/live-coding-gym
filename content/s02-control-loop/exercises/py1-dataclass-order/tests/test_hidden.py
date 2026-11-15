import dataclasses

import pytest

from solution import Version, sort_versions


def test_sort():
    vs = [Version(1, 10, 0), Version(1, 2, 5), Version(0, 9, 9), Version(1, 2, 0)]
    assert sort_versions(vs) == [Version(0, 9, 9), Version(1, 2, 0), Version(1, 2, 5), Version(1, 10, 0)]


def test_compare():
    assert Version(2, 0, 0) > Version(1, 99, 99)
    assert Version(1, 2, 3) == Version(1, 2, 3)
    assert Version(1, 2, 3) < Version(1, 3, 0)


def test_frozen():
    v = Version(1, 0, 0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        v.major = 2


def test_empty_and_input_untouched():
    assert sort_versions([]) == []
    vs = [Version(2, 0, 0), Version(1, 0, 0)]
    sort_versions(vs)
    assert vs == [Version(2, 0, 0), Version(1, 0, 0)]


def test_field_names_and_order():
    assert [f.name for f in dataclasses.fields(Version)] == ["major", "minor", "patch"]
    assert Version(major=2, minor=0, patch=0) > Version(major=1, minor=9, patch=9)
