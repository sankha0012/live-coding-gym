from solution import parse_csv_line


def test_plain():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]


def test_quoted_comma():
    assert parse_csv_line('a,"b,c",d') == ["a", "b,c", "d"]


def test_empty_fields():
    assert parse_csv_line("a,,c") == ["a", "", "c"]
    assert parse_csv_line(",") == ["", ""]


def test_empty_line():
    assert parse_csv_line("") == []
