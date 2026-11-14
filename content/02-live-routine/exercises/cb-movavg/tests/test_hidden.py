import subprocess
import sys

import pytest

CASES = [['3 1 2 3 4 5', '2.00,3.00,4.00'], ['2 10 20', '15.00'], ['5 1 2', 'none']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_io(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.stdout.strip() == want, p.stderr or p.stdout
