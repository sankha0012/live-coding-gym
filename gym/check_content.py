import sys

from . import config
from .content import load_content
from .runner import check_sql, run_python_tests


def check(content_dir):
    steps, problems = load_content(content_dir)
    problems = list(problems)
    for step in steps:
        for ex in step.exercises:
            if ex.kind == "python":
                if not run_python_tests(ex.solution, ex.dir / "tests").passed:
                    problems.append(f"{ex.id}: reference solution fails its own tests")
                if ex.starter and run_python_tests(ex.starter, ex.dir / "tests").passed:
                    problems.append(f"{ex.id}: starter already passes the tests")
            elif ex.kind == "sql":
                if not check_sql(ex.seed, ex.solution, ex.solution, ex.ordered).passed:
                    problems.append(f"{ex.id}: reference solution fails to run")
    return problems


if __name__ == "__main__":
    found = check(config.CONTENT_DIR)
    print("\n".join(found) if found else "content ok")
    sys.exit(1 if found else 0)
