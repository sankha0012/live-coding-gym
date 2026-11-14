from datetime import date, timedelta

from gym import cards

DAY = date(2026, 11, 14)
DECK = [{"id": "a", "front": "f", "back": "b"}, {"id": "b", "front": "f", "back": "b"}]


def test_unseen_cards_are_due(conn):
    assert cards.due(conn, DECK, DAY) == DECK


def test_correct_answers_climb_boxes(conn):
    assert cards.record(conn, "a", True, DAY) == {"box": 1, "due": "2026-11-15"}
    assert cards.record(conn, "a", True, DAY) == {"box": 2, "due": "2026-11-16"}
    assert cards.record(conn, "a", True, DAY) == {"box": 3, "due": "2026-11-18"}


def test_box_is_capped_at_five(conn):
    for _ in range(8):
        r = cards.record(conn, "a", True, DAY)
    assert r == {"box": 5, "due": "2026-11-30"}


def test_wrong_answer_resets_and_stays_due(conn):
    cards.record(conn, "a", True, DAY)
    cards.record(conn, "a", True, DAY)
    assert cards.record(conn, "a", False, DAY) == {"box": 1, "due": "2026-11-14"}
    assert [c["id"] for c in cards.due(conn, DECK, DAY)] == ["a", "b"]


def test_card_returns_on_its_due_date(conn):
    cards.record(conn, "a", True, DAY)
    assert [c["id"] for c in cards.due(conn, DECK, DAY)] == ["b"]
    assert [c["id"] for c in cards.due(conn, DECK, DAY + timedelta(days=1))] == ["a", "b"]
