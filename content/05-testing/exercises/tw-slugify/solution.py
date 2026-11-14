from solution import slugify


def test_lowercases():
    assert slugify("Hello World") == "hello-world"


def test_repeated_spaces():
    assert slugify("a  b") == "a-b"


def test_leading_and_trailing_whitespace():
    assert slugify("  a b  ") == "a-b"


def test_tabs_and_newlines():
    assert slugify("a\tb\nc") == "a-b-c"


def test_empty_and_blank():
    assert slugify("") == ""
    assert slugify("   ") == ""
