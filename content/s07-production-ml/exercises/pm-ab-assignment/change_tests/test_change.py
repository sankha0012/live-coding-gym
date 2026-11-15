from solution import assign

W = {"control": 1, "new": 1}


def test_override_wins_for_every_experiment():
    for exp in ("a", "b", "c", "d"):
        assert assign("qa-1", exp, W, overrides={"qa-1": "new"}) == "new"
        assert assign("qa-2", exp, W, overrides={"qa-2": "control"}) == "control"


def test_override_may_name_a_variant_not_in_weights():
    assert assign("u", "e", {"a": 0, "b": 1}, overrides={"u": "a"}) == "a"
    assert assign("u", "e", W, overrides={"u": "holdout"}) == "holdout"


def test_other_users_are_unchanged():
    ov = {"vip": "new"}
    for i in range(300):
        uid = f"user-{i}"
        assert assign(uid, "exp", W, overrides=ov) == assign(uid, "exp", W)
        assert assign(uid, "exp", W, overrides={}) == assign(uid, "exp", W)
        assert assign(uid, "exp", W, overrides=None) == assign(uid, "exp", W)


def test_override_does_not_touch_the_dict():
    ov = {"vip": "new"}
    assign("vip", "e", W, overrides=ov)
    assign("other", "e", W, overrides=ov)
    assert ov == {"vip": "new"}
