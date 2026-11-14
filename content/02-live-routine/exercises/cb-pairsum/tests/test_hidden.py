import subprocess
import sys

import pytest

CASES = [['1,5,3,7|8', 'true'], ['1,2|5', 'false'], ['4,4|8', 'true'], ['4|8', 'false']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_io(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.stdout.strip() == want, p.stderr or p.stdout
