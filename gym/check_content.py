import re
import sys

from . import config
from .content import load_content
from .kb import load_kb
from .runner import check_sql, run_python_free, run_python_tests, run_test_writing


COMPETENCIES = {f"C{i}" for i in range(1, 11)}


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
        for name, query in ex.wrong.items():
            if check_sql(ex.seed, query, ex.solution, ex.ordered).passed:
                p.append(f"{ex.id}: wrong query {name} gives the reference result")
        for name, query in ex.alt.items():
            if not check_sql(ex.seed, query, ex.solution, ex.ordered).passed:
                p.append(f"{ex.id}: alternative query {name} does not match the reference")
    elif ex.kind == "tests":
        if not run_test_writing(ex.solution, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: reference tests do not catch every bug (or fail on the good implementation)")
        if ex.starter and run_test_writing(ex.starter, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: starter already passes")
    if ex.kind == "read":
        norm = lambda t: "\n".join(x.rstrip() for x in t.strip().splitlines())
        base = run_python_free(ex.snippet, timeout=60)
        if not base.passed or norm(base.output) != norm(ex.expected):
            p.append(f"{ex.id}: snippet output differs from expected.txt")
        if ex.level >= 3 and not ex.questions:
            p.append(f"{ex.id}: a level 3 reading needs questions")
        answers = {v["answer"] for v in ex.whatif}
        if len(ex.whatif) < 4 or "same" not in answers or not answers & {"different", "crash"}:
            p.append(f"{ex.id}: whatif.yaml needs 4+ changes, with outcomes that stay the same and ones that do not")
        for v in ex.whatif:
            if ex.snippet.count(v["old"]) != 1:
                p.append(f"{ex.id}: whatif old text must appear exactly once in the snippet: {v['old']!r}")
                continue
            r = run_python_free(ex.snippet.replace(v["old"], v["new"], 1), timeout=60)
            got = "crash" if not r.passed else "same" if norm(r.output) == norm(base.output) else "different"
            if got != v["answer"]:
                p.append(f"{ex.id}: whatif {v['change']!r} really gives {got}, not {v['answer']}")
        if ex.level >= 3:
            if not (ex.fix and ex.fix_expected and ex.fix_solution):
                p.append(f"{ex.id}: a level 3 reading needs fix.md, fix_expected.txt and fix_solution.py")
            else:
                fixed = run_python_free(ex.fix_solution, timeout=60)
                if not fixed.passed or norm(fixed.output) != norm(ex.fix_expected):
                    p.append(f"{ex.id}: fix_solution.py does not print fix_expected.txt")
                if norm(base.output) == norm(ex.fix_expected):
                    p.append(f"{ex.id}: the snippet already prints fix_expected.txt")
    if ex.kind == "triage":
        verdicts = {x["correct"] for x in ex.proposals}
        if len(ex.proposals) < 3 or verdicts != {"accept", "reject"}:
            p.append(f"{ex.id}: triage needs 3+ proposals with both accept and reject")
        if any(not x.get("why") for x in ex.proposals):
            p.append(f"{ex.id}: every proposal needs a why")
    if ex.name_bug and ex.starter:
        if ex.kind == "sql":
            if check_sql(ex.seed, ex.starter, ex.solution, ex.ordered).passed:
                p.append(f"{ex.id}: buggy starter query already gives the reference result")
        elif run_python_tests(ex.starter, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: buggy starter passes the tests")
    if ex.serves and not set(ex.serves) <= COMPETENCIES:
        p.append(f"{ex.id}: serves must be from C1..C10, got {ex.serves}")
    if ex.change and ex.kind == "sql":
        if not check_sql(ex.seed, ex.change_solution, ex.change_solution, ex.ordered).passed:
            p.append(f"{ex.id}: change_solution.sql fails to run")
        if check_sql(ex.seed, ex.solution, ex.change_solution, ex.ordered).passed:
            p.append(f"{ex.id}: the unchanged solution already gives the change_solution result")
    elif ex.change:
        if not run_python_tests(ex.change_solution, ex.change_dir, files=ex.files).passed:
            p.append(f"{ex.id}: change_solution fails change_tests")
        if run_python_tests(ex.solution, ex.change_dir, files=ex.files).passed:
            p.append(f"{ex.id}: change_tests pass on the unchanged solution")
        if not run_python_tests(ex.change_solution, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: change_solution breaks the hidden tests")
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


def check_curriculum(steps):
    """Rules for the real curriculum (not for tiny test fixtures): every exercise names the competencies it
    serves, every core build proves control, every mock task ships its documentation page."""
    p = []
    for step in steps:
        for ex in step.exercises:
            if not ex.serves:
                p.append(f"{ex.id}: missing serves (competency tags)")
            if ex.mock and not ex.docs:
                p.append(f"{ex.id}: a mock task needs docs.md")
            if ex.control_level >= 2 and not ex.change:
                p.append(f"{ex.id}: a level {ex.control_level} build needs a change to make by hand (change.md)")
            if ex.change and ex.control_level < 2:
                p.append(f"{ex.id}: change.md is never used here (only core builds at level 2 or 3 ask for a change)")
    return p


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
    found = check(config.CONTENT_DIR) + check_curriculum(load_content(config.CONTENT_DIR)[0])
    print("\n".join(found) if found else "content ok")
    sys.exit(1 if found else 0)
