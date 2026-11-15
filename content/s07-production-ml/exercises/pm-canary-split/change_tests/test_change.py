from solution import assign_arm

IDS = [f"user-{i}" for i in range(2000)]


def test_forced_user_is_canary_even_at_zero_percent():
    assert assign_arm("qa-1", 0, force_canary={"qa-1"}) == "canary"
    assert assign_arm("qa-1", 0, "canary-v1", ("qa-1", "qa-2")) == "canary"
    assert assign_arm("qa-2", 0, force_canary=["qa-1", "qa-2"]) == "canary"


def test_other_users_are_unchanged():
    forced = {"qa-1"}
    for u in IDS:
        assert assign_arm(u, 30, force_canary=forced) == assign_arm(u, 30)
    assert {assign_arm(u, 0, force_canary=forced) for u in IDS[:300]} == {"stable"}


def test_forced_users_among_many_get_canary_at_any_percent():
    forced = set(IDS[:200])
    for pct in (0, 5, 50):
        assert {assign_arm(u, pct, force_canary=forced) for u in forced} == {"canary"}
    rest = IDS[200:]
    assert [assign_arm(u, 5, force_canary=forced) for u in rest] == [assign_arm(u, 5) for u in rest]


def test_empty_force_list_changes_nothing():
    for u in IDS[:300]:
        assert assign_arm(u, 40, force_canary=()) == assign_arm(u, 40)
        assert assign_arm(u, 40, "s", set()) == assign_arm(u, 40, "s")
