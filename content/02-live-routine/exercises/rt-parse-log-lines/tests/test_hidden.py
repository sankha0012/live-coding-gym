from solution import parse_logs


def test_basic():
    lines = [
        "2026-08-01T10:00:00 ERROR disk full",
        "2026-08-01T10:00:01 INFO started",
        "2026-08-01T10:00:02 ERROR timeout",
    ]
    assert parse_logs(lines) == ({"ERROR": 2, "INFO": 1}, ["disk full", "timeout"])


def test_message_keeps_spaces():
    assert parse_logs(["2026-08-01T10:00:00 ERROR a b c d"]) == ({"ERROR": 1}, ["a b c d"])


def test_malformed_skipped():
    lines = ["garbage", "2026-08-01T10:00:00 ERROR", "2026-08-01T10:00:01 WARN slow"]
    assert parse_logs(lines) == ({"WARN": 1}, [])


def test_empty():
    assert parse_logs([]) == ({}, [])
