import subprocess
import sys

import pytest

CASES = [['fun&!! time', 'time'], ['I love dogs', 'love'], ['a bb ccc dd', 'ccc'], ['hi!!!!!! yo', 'hi'], ['a12 bc', 'a12'], ["it's ab", 'its'], ['x, yy; zz', 'yy'], ['!!! ???', ''], ['abc def', 'abc'], ['a_b cc', 'ab'], ['"hello," she said', 'hello'], ['a-b c', 'ab']]


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
