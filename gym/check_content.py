import re
import sys

from . import config
from .content import load_content
from .kb import load_kb
from .runner import check_sql, run_python_tests, run_test_writing


def check_exercise(ex):
    p = []
    if ex.kind != "quiz" and not ex.say:
        p.append(f"{ex.id}: missing say.md")
    if ex.kind in ("python", "sql", "tests") and not ex.hint:
        p.append(f"{ex.id}: missing hint.md")
    if ex.kind in ("python", "sql", "tests") and not ex.guide:
        p.append(f"{ex.id}: missing guide.md")
    if ex.kind == "python":
        if not run_python_tests(ex.solution, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: reference solution fails its own tests")
        if ex.starter and run_python_tests(ex.starter, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: starter already passes the tests")
        for name, code in ex.wrong.items():
            if run_python_tests(code, ex.dir / "tests", files=ex.files).passed:
                p.append(f"{ex.id}: wrong solution {name} passes the tests")
    elif ex.kind == "sql":
        if not check_sql(ex.seed, ex.solution, ex.solution, ex.ordered).passed:
            p.append(f"{ex.id}: reference solution fails to run")
    elif ex.kind == "tests":
        if not run_test_writing(ex.solution, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: reference tests do not catch every bug (or fail on the good implementation)")
        if ex.starter and run_test_writing(ex.starter, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: starter already passes")
    return p


KB_LINK = re.compile(r"#/kb/([a-z0-9-]+)")


def check_kb(content_dir, steps):
    """Knowledge-base problems: broken articles, links to missing topics, exercises naming missing topics."""
    topics, problems = load_kb(content_dir)
    problems = list(problems)
    texts = [(f"kb {t.id}", t.body) for t in topics.values()]
    texts += [(f"{s.id} lesson {l['id']}", l["body"]) for s in steps for l in s.lessons]
    for where, text in texts:
        for target in sorted(set(KB_LINK.findall(text))):
            if target not in topics:
                problems.append(f"{where}: link to missing kb topic {target}")
    for s in steps:
        for ex in s.exercises:
            for i in ex.kb:
                if i not in topics:
                    problems.append(f"{ex.id}: unknown kb topic {i}")
    return problems


def check(content_dir):
    steps, problems = load_content(content_dir)
    problems = list(problems)
    seen_ex, seen_cards = {}, {}
    for step in steps:
        for card in step.cards:
            if card["id"] in seen_cards:
                problems.append(f"card {card['id']}: duplicate id (also in {seen_cards[card['id']]})")
            seen_cards[card["id"]] = step.id
        for ex in step.exercises:
            if ex.id in seen_ex:
                problems.append(f"{ex.id}: duplicate exercise id (also in {seen_ex[ex.id]})")
            seen_ex[ex.id] = step.id
            problems += check_exercise(ex)
    return problems + check_kb(content_dir, steps)


if __name__ == "__main__":
    found = check(config.CONTENT_DIR)
    print("\n".join(found) if found else "content ok")
    sys.exit(1 if found else 0)
