import subprocess
import sys

import pytest

CASES = [['1,5,3,7|8', 'true'], ['1,2|5', 'false'], ['4,4|8', 'true'], ['4|8', 'false'], ['-3,7|4', 'true'], ['0,0|0', 'true'], ['0|0', 'false'], ['1,2,3|10', 'false'], ['5,3|8', 'true'], ['3,5|8', 'true'], ['2,2,2|4', 'true'], ['5|10', 'false'], ['1,9,5|10', 'true'], ['1,2,3|6', 'false'], ['9,1,5,5|10', 'true'], ['1,2,3|0', 'false'], ['-5,5|0', 'true'], ['3,9,1,2|3', 'true'], ['7,1,5|13', 'false'], ['1,5,9|10', 'true'], ['4,1,2,6|10', 'true']]


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
