import os
import time
from datetime import datetime, timedelta, timezone

import pytest
from solution import is_expired

BRT = timezone(timedelta(hours=-3))


@pytest.fixture(autouse=True)
def fixed_local_zone():
    old = os.environ.get("TZ")
    os.environ["TZ"] = "America/Sao_Paulo"
    time.tzset()
    yield
    if old is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = old
    time.tzset()


def test_both_naive():
    assert is_expired(datetime(2024, 1, 1, 12), datetime(2024, 1, 1, 12))
    assert not is_expired(datetime(2024, 1, 1, 12), datetime(2024, 1, 1, 11))


def test_mixed_naive_and_aware_utc():
    exp = datetime(2024, 1, 1, 12)
    now = datetime(2024, 1, 1, 12, 1, tzinfo=timezone.utc)
    assert is_expired(exp, now)


def test_aware_other_zone_is_converted():
    exp = datetime(2024, 1, 1, 12, tzinfo=BRT)  # 15:00 UTC
    assert not is_expired(exp, datetime(2024, 1, 1, 14, 59, tzinfo=timezone.utc))
    assert is_expired(exp, datetime(2024, 1, 1, 15, 0, tzinfo=timezone.utc))


def test_naive_is_utc_not_local():
    exp = datetime(2024, 1, 1, 12)  # 12:00 UTC
    assert is_expired(exp, datetime(2024, 1, 1, 9, 0, tzinfo=BRT))  # 12:00 UTC
    assert not is_expired(exp, datetime(2024, 1, 1, 8, 59, tzinfo=BRT))


def test_inputs_unchanged():
    exp = datetime(2024, 1, 1, 12, tzinfo=BRT)
    is_expired(exp, datetime(2024, 1, 2))
    assert exp.tzinfo is BRT
