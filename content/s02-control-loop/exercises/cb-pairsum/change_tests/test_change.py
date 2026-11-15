import subprocess
import sys

import pytest

CASES = [['4,4|8|distinct', 'false'], ['0,0|0|distinct', 'false'], ['1,5,3,7|8|distinct', 'true'], ['2,2,6|8|distinct', 'true'], ['4,4,4|8|distinct', 'false'], ['4,4|8', 'true'], ['5|10|distinct', 'false'], ['3,3,5|8|distinct', 'true']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_change(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.returncode == 0, p.stderr
    assert p.stdout.strip() == want
