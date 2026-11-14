import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunResult:
    passed: bool
    tests: list = field(default_factory=list)
    output: str = ""
    timed_out: bool = False


def run_python_tests(code, tests_dir, timeout=10, files=()):
    """Run hidden pytest tests against a submission saved as solution.py."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "solution.py").write_text(code)
        shutil.copytree(tests_dir, tmp / "tests")
        for f in files:
            shutil.copy(f, tmp / Path(f).name)
        cmd = [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short",
               "-p", "no:cacheprovider", "--junitxml=report.xml"]
        try:
            # `python -m pytest` puts the working directory on sys.path,
            # which is what lets the tests `from solution import ...`.
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        tests = []
        report = tmp / "report.xml"
        if report.exists():
            for case in ET.parse(report).iter("testcase"):
                failed = case.find("failure") is not None or case.find("error") is not None
                tests.append({"name": case.get("name"), "passed": not failed})
        return RunResult(proc.returncode == 0, tests, proc.stdout + proc.stderr)


def run_python_free(code, timeout=10):
    """Run code as a script with no tests, like the Run button on Coderbyte."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "main.py").write_text(code)
        try:
            proc = subprocess.run([sys.executable, "main.py"], cwd=tmp,
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        return RunResult(proc.returncode == 0, [], proc.stdout + proc.stderr)


def _query(seed, sql, timeout):
    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(seed)
        deadline = time.monotonic() + timeout
        # A truthy return from the progress handler aborts the running query.
        conn.set_progress_handler(lambda: time.monotonic() > deadline, 10000)
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description or []]
        return cols, cur.fetchall()
    finally:
        conn.close()


def _table(cols, rows, limit=50):
    lines = [" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows[:limit]]
    if len(rows) > limit:
        lines.append(f"... {len(rows) - limit} more rows")
    return "\n".join(lines)


def run_sql_free(seed, sql, timeout=5):
    try:
        cols, rows = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [], str(e))
    return RunResult(True, [], _table(cols, rows))


def check_sql(seed, sql, solution, ordered=False, timeout=5):
    try:
        cols, got = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [{"name": "result matches reference", "passed": False}], str(e))
    _, want = _query(seed, solution, timeout)

    def norm(rows):
        return rows if ordered else sorted(rows, key=repr)

    passed = norm(got) == norm(want)
    output = _table(cols, got)
    if not passed:
        output += f"\n\nExpected {len(want)} rows, got {len(got)}."
        if ordered and sorted(got, key=repr) == sorted(want, key=repr):
            output += " The rows are right but the order is wrong."
    return RunResult(passed, [{"name": "result matches reference", "passed": passed}], output)
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunResult:
    passed: bool
    tests: list = field(default_factory=list)
    output: str = ""
    timed_out: bool = False


def run_python_tests(code, tests_dir, timeout=10, files=()):
    """Run hidden pytest tests against a submission saved as solution.py."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "solution.py").write_text(code)
        shutil.copytree(tests_dir, tmp / "tests")
        for f in files:
            shutil.copy(f, tmp / Path(f).name)
        cmd = [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short",
               "-p", "no:cacheprovider", "--junitxml=report.xml"]
        try:
            # `python -m pytest` puts the working directory on sys.path,
            # which is what lets the tests `from solution import ...`.
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        tests = []
        report = tmp / "report.xml"
        if report.exists():
            for case in ET.parse(report).iter("testcase"):
                failed = case.find("failure") is not None or case.find("error") is not None
                tests.append({"name": case.get("name"), "passed": not failed})
        return RunResult(proc.returncode == 0, tests, proc.stdout + proc.stderr)


def run_python_free(code, timeout=10):
    """Run code as a script with no tests, like the Run button on Coderbyte."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "main.py").write_text(code)
        try:
            proc = subprocess.run([sys.executable, "main.py"], cwd=tmp,
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        return RunResult(proc.returncode == 0, [], proc.stdout + proc.stderr)


def _query(seed, sql, timeout):
    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(seed)
        deadline = time.monotonic() + timeout
        # A truthy return from the progress handler aborts the running query.
        conn.set_progress_handler(lambda: time.monotonic() > deadline, 10000)
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description or []]
        return cols, cur.fetchall()
    finally:
        conn.close()


def _table(cols, rows, limit=50):
    lines = [" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows[:limit]]
    if len(rows) > limit:
        lines.append(f"... {len(rows) - limit} more rows")
    return "\n".join(lines)


def run_sql_free(seed, sql, timeout=5):
    try:
        cols, rows = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [], str(e))
    return RunResult(True, [], _table(cols, rows))


def check_sql(seed, sql, solution, ordered=False, timeout=5):
    try:
        cols, got = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [{"name": "result matches reference", "passed": False}], str(e))
    _, want = _query(seed, solution, timeout)

    def norm(rows):
        return rows if ordered else sorted(rows, key=repr)

    passed = norm(got) == norm(want)
    output = _table(cols, got)
    if not passed:
        output += f"\n\nExpected {len(want)} rows, got {len(got)}."
        if ordered and sorted(got, key=repr) == sorted(want, key=repr):
            output += " The rows are right but the order is wrong."
    return RunResult(passed, [{"name": "result matches reference", "passed": passed}], output)


def _pytest(files, timeout):
    """Run pytest on test_candidate.py in a temp dir holding `files` (name -> text)."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in files.items():
            (Path(tmp) / name).write_text(text)
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider", "test_candidate.py"]
        try:
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, f"Timed out after {timeout}s"
        return proc.returncode, proc.stdout + proc.stderr


def run_test_writing(test_code, good, bads, timeout=10):
    """Grade a learner's test file: it must pass on `good` and fail on every `bads` implementation."""
    rc, output = _pytest({"solution.py": good, "test_candidate.py": test_code}, timeout)
    good_ok = rc == 0  # exit code 5 (no tests collected) and 2 (import error) do not count
    tests = [{"name": "passes on the correct implementation", "passed": good_ok}]
    for name, bad in bads.items():
        caught = False
        if good_ok:
            bad_rc, _ = _pytest({"solution.py": bad, "test_candidate.py": test_code}, timeout)
            caught = bad_rc == 1
        tests.append({"name": "catches " + name.replace("impl_bad_", "bug "), "passed": caught})
    return RunResult(all(t["passed"] for t in tests), tests, output, rc is None)
