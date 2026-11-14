import pytest

from solution import ConfigError, parse_config


def test_defaults():
    got = parse_config({"name": "api"})
    assert got == {"name": "api", "port": 8080, "debug": False, "timeout_s": 5.0, "tags": []}


def test_full_parse_and_strip():
    raw = {"name": " api ", "port": " 9000 ", "debug": " TRUE ", "timeout_s": "2.5", "tags": "a, b,,c ,"}
    got = parse_config(raw)
    assert got == {"name": "api", "port": 9000, "debug": True, "timeout_s": 2.5, "tags": ["a", "b", "c"]}
    assert raw["name"] == " api "


def test_bool_false_is_false():
    assert parse_config({"name": "x", "debug": "false"})["debug"] is False
    assert parse_config({"name": "x", "debug": "0"})["debug"] is False
    assert parse_config({"name": "x", "debug": "1"})["debug"] is True


def test_reports_every_problem_sorted():
    with pytest.raises(ConfigError) as e:
        parse_config({"port": "99999", "debug": "maybe", "timeout_s": "abc"})
    assert e.value.problems == ["debug: invalid", "name: missing", "port: invalid", "timeout_s: invalid"]
    assert str(e.value) == "debug: invalid; name: missing; port: invalid; timeout_s: invalid"


def test_ranges_and_blanks():
    for key, bad in [("port", "0"), ("port", ""), ("port", "80.5"), ("timeout_s", "0"),
                     ("timeout_s", "nan"), ("timeout_s", "inf"), ("timeout_s", "-1")]:
        with pytest.raises(ConfigError) as e:
            parse_config({"name": "x", key: bad})
        assert e.value.problems == [f"{key}: invalid"], (key, bad)


def test_blank_name_and_unknown_keys():
    with pytest.raises(ConfigError) as e:
        parse_config({"name": "   "})
    assert e.value.problems == ["name: invalid"]
    assert parse_config({"name": "x", "other": "1"})["name"] == "x"


def test_default_list_not_shared():
    a = parse_config({"name": "x"})
    a["tags"].append("z")
    assert parse_config({"name": "x"})["tags"] == []


def test_is_exception_subclass():
    assert issubclass(ConfigError, Exception)


def test_bool_rejects_other_words_and_blank():
    for bad in ["", "  ", "yes", "no", "t", "2", "on"]:
        with pytest.raises(ConfigError) as e:
            parse_config({"name": "x", "debug": bad})
        assert e.value.problems == ["debug: invalid"], bad


def test_empty_tags_and_present_defaults_not_used_for_bad_values():
    assert parse_config({"name": "x", "tags": ""})["tags"] == []
    assert parse_config({"name": "x", "tags": " , ,"})["tags"] == []
    with pytest.raises(ConfigError):
        parse_config({"name": "x", "port": "abc"})


def test_name_missing_and_other_problems_together_even_if_name_blank():
    with pytest.raises(ConfigError) as e:
        parse_config({"name": "", "port": "x"})
    assert e.value.problems == ["name: invalid", "port: invalid"]
