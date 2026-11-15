import subprocess
import sys

import pytest

CASES = [['aabbcde', '2a2b1c1d1e'], ['wwwggopp', '3w2g1o2p'], ['z', '1z'], ['aabaa', '2a1b2a'], ['aaaaaaaaaaaa', '12a'], ['abc', '1a1b1c'], ['', ''], ['aaab', '3a1b'], ['abbb', '1a3b'], ['aaaabbbbcc', '4a4b2c'], ['abab', '1a1b1a1b'], ['xyyz', '1x2y1z']]


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
