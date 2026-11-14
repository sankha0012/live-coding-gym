import subprocess
import sys

import pytest

CASES = [['aabbcde', '2a2b1c1d1e'], ['wwwggopp', '3w2g1o2p'], ['z', '1z']]


@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])
def test_io(stdin, want):
    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\n',
                       capture_output=True, text=True, timeout=5)
    assert p.stdout.strip() == want, p.stderr or p.stdout
