from datetime import datetime, timedelta, timezone

from solution import daily_counts

SP = "America/Sao_Paulo"  # UTC-3, no daylight saving


def test_naive_is_utc_and_shifts_back_a_day():
    # 02:30 UTC is 23:30 the day before in Sao Paulo
    assert daily_counts([datetime(2024, 3, 10, 2, 30)], SP) == {"2024-03-09": 1}


def test_naive_same_local_day():
    ts = [datetime(2024, 3, 10, 12, 0), datetime(2024, 3, 10, 20, 0)]
    assert daily_counts(ts, SP) == {"2024-03-10": 2}


def test_aware_utc_is_converted():
    ts = [datetime(2024, 3, 10, 2, 30, tzinfo=timezone.utc)]
    assert daily_counts(ts, SP) == {"2024-03-09": 1}


def test_aware_other_zone_is_converted():
    plus9 = timezone(timedelta(hours=9))
    # 2024-03-10 08:00 at +09:00 is 2024-03-09 23:00 UTC, 20:00 in Sao Paulo
    assert daily_counts([datetime(2024, 3, 10, 8, 0, tzinfo=plus9)], SP) == {"2024-03-09": 1}


def test_daylight_saving_offset_changes():
    ny = "America/New_York"
    winter = datetime(2024, 1, 15, 4, 30)  # 23:30 on the 14th at UTC-5
    summer = datetime(2024, 7, 15, 4, 30)  # 00:30 on the 15th at UTC-4
    assert daily_counts([winter, summer], ny) == {"2024-01-14": 1, "2024-07-15": 1}


def test_empty():
    assert daily_counts([], SP) == {}
