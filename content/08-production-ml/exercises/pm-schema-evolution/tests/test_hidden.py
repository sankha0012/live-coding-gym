import copy

import pytest
from solution import parse_event

V2 = {"version": 2, "user_id": "u1", "amount_cents": 1250, "currency": "USD"}


def test_v2_passthrough():
    assert parse_event(V2) == V2


def test_v1_upgrade():
    assert parse_event({"version": 1, "user_id": "u1", "amount": 12.5}) == {
        "version": 2, "user_id": "u1", "amount_cents": 1250, "currency": "BRL"}


@pytest.mark.parametrize("amount,cents", [(19.99, 1999), (0.29, 29), (0, 0), (3, 300), (1.15, 115)])
def test_v1_rounding(amount, cents):
    got = parse_event({"version": 1, "user_id": "u", "amount": amount})
    assert got["amount_cents"] == cents
    assert isinstance(got["amount_cents"], int)


def test_extra_keys_dropped():
    got = parse_event({**V2, "debug": True})
    assert set(got) == {"version", "user_id", "amount_cents", "currency"}


def test_input_not_mutated():
    p1 = {"version": 1, "user_id": "u", "amount": 5.0}
    p2 = dict(V2, extra=1)
    s1, s2 = copy.deepcopy(p1), copy.deepcopy(p2)
    parse_event(p1)
    parse_event(p2)
    assert p1 == s1 and p2 == s2


@pytest.mark.parametrize("bad", [
    {"user_id": "u", "amount": 1.0},
    {"version": 3, "user_id": "u", "amount_cents": 1, "currency": "USD"},
    {"version": "1", "user_id": "u", "amount": 1.0},
    {"version": 1, "amount": 1.0},
    {"version": 1, "user_id": "u"},
    {"version": 1, "user_id": "u", "amount": "12.5"},
    {"version": 2, "user_id": "u", "currency": "USD"},
    {"version": 2, "user_id": "u", "amount_cents": 12.5, "currency": "USD"},
    {"version": 2, "user_id": "u", "amount_cents": True, "currency": "USD"},
    {"version": 2, "user_id": "u", "amount_cents": 5},
    [],
    None,
])
def test_rejected(bad):
    with pytest.raises(ValueError):
        parse_event(bad)


@pytest.mark.parametrize("amount,cents", [(-19.99, -1999), (-0.29, -29), (-3, -300)])
def test_v1_negative_amounts_round_to_nearest(amount, cents):
    assert parse_event({"version": 1, "user_id": "u", "amount": amount})["amount_cents"] == cents


def test_v1_extra_keys_dropped_too():
    got = parse_event({"version": 1, "user_id": "u", "amount": 2.5, "debug": 1, "amount_cents": 7})
    assert got == {"version": 2, "user_id": "u", "amount_cents": 250, "currency": "BRL"}


@pytest.mark.parametrize("bad", [
    {"version": True, "user_id": "u", "amount": 1.0},
    {"version": 1, "user_id": 5, "amount": 1.0},
    {"version": 1, "user_id": None, "amount": 1.0},
    {"version": 1, "user_id": "u", "amount": True},
    {"version": 1, "user_id": "u", "amount": None},
    {"version": 2, "user_id": 5, "amount_cents": 1, "currency": "USD"},
    {"version": 2, "user_id": "u", "amount_cents": 1, "currency": 5},
    {"version": 2, "user_id": "u", "amount_cents": 1, "currency": None},
    {"version": 2, "user_id": "u", "amount_cents": 1250.0, "currency": "USD"},
    {"version": 2, "user_id": "u", "amount_cents": None, "currency": "USD"},
])
def test_more_rejected(bad):
    with pytest.raises(ValueError):
        parse_event(bad)
