"""One-off: convert tools/old_gym.json (export of the old single-file gym) into content/ folders.

Run: uv run python tools/migrate_old_gym.py
Existing files are never overwritten, so it is safe to re-run after hand edits.
"""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("01-hand-python", "Hand-coding Python from zero", 1, 4, True),
    ("02-live-routine", "The live-coding routine", 2, 4, True),
    ("03-hand-sql", "Hand-coding SQL", 3, 4, True),
    ("04-robust-code", "Robust code", 4, 4, False),
    ("05-testing", "Testing your own code", 5, 4, False),
    ("06-real-data", "Real data behaviour and statistics", 6, 4, False),
    ("07-ml-tools", "AI/ML engineering tools tour", 7, 4, False),
    ("08-production-ml", "Production ML systems", 8, 4, False),
    ("09-model-failures", "Common model failures", 9, 4, False),
    ("10-ai-assistant", "Using an AI assistant while observed", 10, 4, False),
    ("11-explaining", "Explaining your code", 11, 4, False),
    ("12-mock-rounds", "Mock rounds and readiness", 12, 4, False),
]

DRILL_STEP = {}
for step, ids in {
    "01-hand-python": "py-second py-avg py-newret py-city py-latest py-topk py-session py-merge py-window py-assign",
    "02-live-routine": "cb-fact cb-longest cb-rle cb-brackets cb-sumkeys cb-pairsum cb-movavg cb-wordfreq",
    "03-hand-sql": "sql-cancel sql-slow sql-top2 sql-second sql-mom sql-coupon sql-loyal sql-second-order sql-late sql-churn",
    "04-robust-code": "prod-validate prod-batch prod-split prod-breaker prod-events ai-retry",
    "06-real-data": "st-meanstd st-auc st-z st-ks st-boot dbg-avg dbg-late dbg-tags",
    "08-production-ml": "prod-monitor prod-debug ai-psi ai-eval ai-prf",
    "10-ai-assistant": "ai-topk ai-chunk ai-json ai-trim",
}.items():
    DRILL_STEP.update({i: step for i in ids.split()})

LESSON_STEP = {"routine": "02-live-routine", "coderbyte": "02-live-routine", "patterns": "02-live-routine",
               "python": "01-hand-python", "sql": "03-hand-sql", "robust": "04-robust-code",
               "pandas": "06-real-data", "traps": "06-real-data", "stats": "06-real-data",
               "ai": "10-ai-assistant", "senior": "11-explaining", "phrases": "11-explaining"}
CARD_STEP = {"Python": "01-hand-python", "SQL": "03-hand-sql", "pandas": "06-real-data", "Stats": "06-real-data"}
FACTOR = {"01-hand-python": 2, "03-hand-sql": 2}

CLOSE = '''def _close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-6 + 1e-9 * abs(b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_close(a[k], b[k]) for k in a)
    return a == b
'''


def checks_tests(d):
    """Old behaviour: exec the submission, then the drill's setup code, in one namespace; eval each check."""
    out = [CLOSE, "PRE = " + repr(d.get("pre", "")), "",
           "def _ns():", "    ns = {'__name__': '__main__'}",
           "    exec(open('solution.py').read() + '\\n\\n' + PRE, ns)", "    return ns", ""]
    for i, (expr, want) in enumerate(d["checks"], 1):
        out += [f"def test_check_{i}():", "    ns = _ns()", f"    got = eval({expr!r}, ns)",
                f"    assert _close(got, eval({want!r}, ns)), repr(got)", ""]
    return "\n".join(out)


def io_tests(d):
    return ("import subprocess\nimport sys\n\nimport pytest\n\n"
            "CASES = " + repr(d["io"]) + "\n\n\n"
            "@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])\n"
            "def test_io(stdin, want):\n"
            "    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\\n',\n"
            "                       capture_output=True, text=True, timeout=5)\n"
            "    assert p.stdout.strip() == want, p.stderr or p.stdout\n")


def write(path, text, only_missing):
    if only_missing and path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_drill(out, step, d, is_mock, schema, only_missing):
    ex = out / step / "exercises" / d["id"]
    kind = "sql" if "ref" in d else "python"
    meta = {"title": d["title"], "kind": kind, "required": True, "mock": is_mock,
            "time_limit_s": round(d["mins"] * 60 * FACTOR.get(step, 1.5))}
    prompt = d["pt"] + ("\n\n*" + d["en"] + "*" if d.get("en") else "")
    if kind == "sql":
        meta.update(ordered=bool(d.get("ordered")), seed_file="../../../_shared/delivery.sql")
        prompt += "\n\nTables:\n\n```\n" + schema + "\n```"
        write(ex / "starter.sql", d["starter"], only_missing)
        write(ex / "solution.sql", d["ref"], only_missing)
    else:
        write(ex / "starter.py", d["starter"], only_missing)
        write(ex / "solution.py", d["solution"], only_missing)
        write(ex / "tests" / "test_hidden.py", io_tests(d) if "io" in d else checks_tests(d), only_missing)
    write(ex / "exercise.yaml", yaml.safe_dump(meta, sort_keys=False), only_missing)
    write(ex / "prompt.md", prompt + "\n", only_missing)
    for name, key in (("hint.md", "hint"), ("say.md", "say"), ("model_prompt.md", "prompt")):
        if d.get(key):
            write(ex / name, d[key] + "\n", only_missing)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def migrate(old, out, only_missing=True):
    out = Path(out)
    for folder, title, order, min_score, timed in STEPS:
        meta = {"title": title, "order": order, "gate": {"min_score": min_score, "timed_required": timed}}
        write(out / folder / "step.yaml", yaml.safe_dump(meta, sort_keys=False), only_missing)
    mock_ids = {i for m in old["MOCKS"] for i in (m.get("drills") or [])}
    manual = []
    for d in old["DRILLS"]:
        step = DRILL_STEP.get(d["id"])
        if step is None:
            manual.append(d["id"])
            continue
        write_drill(out, step, d, d["id"] in mock_ids, old["SCHEMA"], only_missing)
    for n, lesson in enumerate(old["LESSONS"], 1):
        step = LESSON_STEP[lesson["id"]]
        title = re.sub(r"^\d+b? · ", "", lesson["title"])
        write(out / step / "lessons" / f"{n:02d}-{lesson['id']}.md", f"# {title}\n\n{lesson['html']}\n", only_missing)
    cards = {}
    for front, back in old["CARDS"]:
        step = CARD_STEP[front.split(" · ")[0]]
        cards.setdefault(step, []).append({"id": slug(front), "front": front, "back": back})
    for step, items in cards.items():
        write(out / step / "cards.yaml", yaml.safe_dump(items, sort_keys=False, allow_unicode=True), only_missing)
    return manual


def main():
    old = json.loads((ROOT / "tools" / "old_gym.json").read_text())
    manual = migrate(old, ROOT / "content")
    print("left for hand conversion:", ", ".join(manual))


if __name__ == "__main__":
    main()
