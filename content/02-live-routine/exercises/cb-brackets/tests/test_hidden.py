import subprocess
import sys

import pytest

CASES = [['(hello [world])', 'true'], ['(]', 'false'], ['((', 'false'], ['no brackets', 'true'], ['{[()()]}', 'true'], ['([)]', 'false'], [')(', 'false'], [')', 'false'], ['(()', 'false'], ['{[}', 'false'], ['', 'true'], ['[({})]', 'true'], ['a)b(', 'false'], ['}{', 'false'], ['([]', 'false']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_io(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.stdout.strip() == want, p.stderr or p.stdout


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_no_crash(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.returncode == 0, p.stderr
