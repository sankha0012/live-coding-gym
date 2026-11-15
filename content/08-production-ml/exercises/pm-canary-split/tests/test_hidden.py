import os
import subprocess
import sys

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


def test_default_salt_is_canary_v1():
    for u in IDS[:500]:
        assert assign_arm(u) == assign_arm(u, 5, "canary-v1")
        assert assign_arm(u, 50) == assign_arm(u, 50, salt="canary-v1")


def test_same_in_every_process():
    here = os.path.dirname(os.path.abspath(__import__("solution").__file__))
    code = "from solution import assign_arm;print([assign_arm(f'u{i}', 50) for i in range(60)])"
    outs = set()
    for seed in ("1", "2", "3"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run([sys.executable, "-c", code], cwd=here, env=env,
                           capture_output=True, text=True, timeout=5)
        assert r.returncode == 0, r.stderr
        outs.add(r.stdout)
    assert len(outs) == 1


def test_share_even_at_other_percents():
    for pct, lo, hi in ((10, 0.09, 0.11), (25, 0.235, 0.265)):
        share = sum(assign_arm(u, pct) == "canary" for u in IDS) / len(IDS)
        assert lo <= share <= hi, pct
