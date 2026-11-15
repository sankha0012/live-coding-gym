import subprocess
import sys

import pytest

CASES = [['3 1 2 3 4 5', '2.00,3.00,4.00'], ['2 10 20', '15.00'], ['5 1 2', 'none'], ['1 5 6 7', '5.00,6.00,7.00'], ['3 1 2 3', '2.00'], ['2 1 2 4', '1.50,3.00'], ['3 1 1 2', '1.33'], ['2 -1 1 3', '0.00,2.00'], ['2 1.5 2.5 3.5', '2.00,3.00'], ['2 1 2', '1.50'], ['2 1', 'none'], ['3 1 2 4 8 16', '2.33,4.67,9.33']]


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
