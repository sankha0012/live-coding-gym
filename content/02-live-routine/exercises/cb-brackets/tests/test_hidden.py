import subprocess
import sys

import pytest

CASES = [['(hello [world])', 'true'], ['(]', 'false'], ['((', 'false'], ['no brackets', 'true'], ['{[()()]}', 'true']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_io(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.stdout.strip() == want, p.stderr or p.stdout
