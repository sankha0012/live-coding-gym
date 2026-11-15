from datetime import datetime, timedelta

import pytest

from solution import check_staleness

NOW = datetime(2026, 11, 14, 12, 0, 0)


def test_fresh():
    r = check_staleness(NOW - timedelta(days=2), NOW - timedelta(days=5), NOW, 30, 14)
    assert r["model_age_days"] == pytest.approx(2.0)
    assert r["data_age_days"] == pytest.approx(5.0)
    assert r["model_stale"] is False and r["data_stale"] is False


def test_model_stale_data_fresh():
    r = check_staleness(NOW - timedelta(days=40), NOW - timedelta(days=1), NOW, 30, 14)
    assert r["model_stale"] is True and r["data_stale"] is False


def test_fractional_age_counts():
    r = check_staleness(NOW - timedelta(days=7, hours=12), NOW, NOW, 7, 1)
    assert r["model_stale"] is True


def test_exactly_at_limit_is_ok():
    r = check_staleness(NOW - timedelta(days=30), NOW - timedelta(days=14), NOW, 30, 14)
    assert r["model_stale"] is False and r["data_stale"] is False


def test_data_stale():
    r = check_staleness(NOW, NOW - timedelta(days=90), NOW, 30, 14)
    assert r["data_stale"] is True and r["model_stale"] is False


def test_future_timestamp_raises():
    with pytest.raises(ValueError):
        check_staleness(NOW + timedelta(seconds=1), NOW, NOW, 30, 14)
    with pytest.raises(ValueError):
        check_staleness(NOW, NOW + timedelta(days=1), NOW, 30, 14)


def test_ages_keep_the_fraction():
    r = check_staleness(NOW - timedelta(days=2, hours=12), NOW - timedelta(hours=6), NOW, 30, 14)
    assert r["model_age_days"] == pytest.approx(2.5)
    assert r["data_age_days"] == pytest.approx(0.25)


def test_each_age_uses_its_own_limit():
    r = check_staleness(NOW - timedelta(days=5), NOW - timedelta(days=1), NOW, 3, 30)
    assert r["model_stale"] is True and r["data_stale"] is False
    r = check_staleness(NOW - timedelta(days=1), NOW - timedelta(days=5), NOW, 30, 3)
    assert r["model_stale"] is False and r["data_stale"] is True
