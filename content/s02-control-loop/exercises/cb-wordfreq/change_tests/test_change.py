import subprocess
import sys

import pytest

CASES = [['', 'none'], ['   ', 'none'], ['!!! ...', 'none'], ['Hello', 'hello'], ['b a b a', 'a']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_change(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.returncode == 0, p.stderr
    assert p.stdout.strip() == want
