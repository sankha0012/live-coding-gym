from datetime import datetime, timedelta

import pytest

from solution import check_staleness

NOW = datetime(2026, 11, 14, 12, 0, 0)


def test_grace_makes_slightly_old_model_ok():
    r = check_staleness(NOW - timedelta(days=31), NOW, NOW, 30, 14, grace_days=2)
    assert r["model_stale"] is False


def test_beyond_limit_plus_grace_is_stale():
    r = check_staleness(NOW - timedelta(days=33), NOW, NOW, 30, 14, grace_days=2)
    assert r["model_stale"] is True


def test_exactly_limit_plus_grace_is_ok():
    r = check_staleness(NOW - timedelta(days=32), NOW - timedelta(days=16), NOW, 30, 14, grace_days=2)
    assert r["model_stale"] is False and r["data_stale"] is False


def test_grace_applies_to_data_too():
    r = check_staleness(NOW, NOW - timedelta(days=15), NOW, 30, 14, grace_days=2)
    assert r["data_stale"] is False
    r = check_staleness(NOW, NOW - timedelta(days=17), NOW, 30, 14, grace_days=2)
    assert r["data_stale"] is True


def test_ages_are_not_changed_by_grace():
    r = check_staleness(NOW - timedelta(days=31), NOW - timedelta(days=1), NOW, 30, 14, grace_days=2)
    assert r["model_age_days"] == pytest.approx(31.0)
    assert r["data_age_days"] == pytest.approx(1.0)


def test_future_timestamp_still_raises():
    with pytest.raises(ValueError):
        check_staleness(NOW + timedelta(seconds=1), NOW, NOW, 30, 14, grace_days=2)
