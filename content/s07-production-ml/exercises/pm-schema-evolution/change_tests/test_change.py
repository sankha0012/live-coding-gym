import copy

import pytest
from solution import parse_event


def test_v1_currency_used():
    got = parse_event({"version": 1, "user_id": "u", "amount": 2.5, "currency": "USD"})
    assert got == {"version": 2, "user_id": "u", "amount_cents": 250, "currency": "USD"}


@pytest.mark.parametrize("cur", [None, 5, ["USD"]])
def test_v1_non_string_currency_falls_back(cur):
    got = parse_event({"version": 1, "user_id": "u", "amount": 1.0, "currency": cur})
    assert got["currency"] == "BRL"
    assert got["amount_cents"] == 100


def test_v1_without_currency_still_brl():
    assert parse_event({"version": 1, "user_id": "u", "amount": 1.0})["currency"] == "BRL"


def test_v1_currency_input_not_mutated_and_keys_exact():
    p = {"version": 1, "user_id": "u", "amount": 19.99, "currency": "EUR", "x": 1}
    before = copy.deepcopy(p)
    got = parse_event(p)
    assert p == before
    assert set(got) == {"version", "user_id", "amount_cents", "currency"}
    assert got["amount_cents"] == 1999
