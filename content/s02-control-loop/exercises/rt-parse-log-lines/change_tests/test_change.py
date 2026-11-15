from solution import parse_logs

LINES = [
    "2026-08-01T10:00:00 ERROR disk full",
    "2026-08-01T10:00:01 WARN slow",
    "2026-08-01T10:00:02 WARN very slow",
    "bad line",
    "2026-08-01T10:00:03 INFO ok",
]


def test_warn_messages():
    counts, msgs = parse_logs(LINES, level="WARN")
    assert counts == {"ERROR": 1, "WARN": 2, "INFO": 1}
    assert msgs == ["slow", "very slow"]


def test_info_messages():
    assert parse_logs(LINES, level="INFO")[1] == ["ok"]


def test_unknown_level_gives_no_messages():
    assert parse_logs(LINES, level="DEBUG")[1] == []


def test_error_not_collected_for_other_level():
    assert "disk full" not in parse_logs(LINES, level="WARN")[1]


def test_default_still_error():
    assert parse_logs(LINES)[1] == ["disk full"]
