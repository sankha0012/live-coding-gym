from solution import parse_config


def test_tags_are_lowercased():
    got = parse_config({"name": "x", "tags": " API, Web ,,Db "})
    assert got["tags"] == ["api", "web", "db"]


def test_lowercase_keeps_order_and_duplicates():
    assert parse_config({"name": "x", "tags": "B, a ,b,,C"})["tags"] == ["b", "a", "b", "c"]


def test_name_keeps_its_case_and_default_tags():
    got = parse_config({"name": " MyApi "})
    assert got["name"] == "MyApi" and got["tags"] == []
