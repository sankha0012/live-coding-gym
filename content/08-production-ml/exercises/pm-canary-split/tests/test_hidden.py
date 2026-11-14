from solution import assign_arm

IDS = [f"user-{i}" for i in range(10000)]


def test_sticky():
    first = [assign_arm(u) for u in IDS[:500]]
    second = [assign_arm(u) for u in IDS[:500]]
    assert first == second


def test_about_five_percent():
    share = sum(assign_arm(u) == "canary" for u in IDS) / len(IDS)
    assert 0.045 <= share <= 0.055


def test_zero_and_hundred():
    assert {assign_arm(u, 0) for u in IDS[:300]} == {"stable"}
    assert {assign_arm(u, 100) for u in IDS[:300]} == {"canary"}


def test_only_adds_users_when_percent_grows():
    small = {u for u in IDS if assign_arm(u, 5) == "canary"}
    big = {u for u in IDS if assign_arm(u, 10) == "canary"}
    assert small < big


def test_percent_is_respected():
    share = sum(assign_arm(u, 50) == "canary" for u in IDS) / len(IDS)
    assert 0.47 <= share <= 0.53


def test_salt_reshuffles():
    a = [assign_arm(u, 50, salt="a") for u in IDS[:1000]]
    b = [assign_arm(u, 50, salt="b") for u in IDS[:1000]]
    assert a != b
    assert 300 < sum(x != y for x, y in zip(a, b)) < 700


def test_empty_id_and_return_values():
    assert assign_arm("") in {"canary", "stable"}
    assert {assign_arm(u, 50) for u in IDS[:50]} == {"canary", "stable"}
