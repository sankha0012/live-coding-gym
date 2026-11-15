import subprocess
import sys

import pytest

CASES = [['a:1,b:2,a:3', 'a:4,b:2'], ['x:5', 'x:5'], ['b:1,a:1,b:-1', 'a:1,b:0'], ['b:2,a:1', 'a:1,b:2'], ['a:1,a:1,a:1', 'a:3'], ['a:10,a:5', 'a:15'], ['ab:1,a:2', 'a:2,ab:1'], ['c:3,b:2,a:1,c:1', 'a:1,b:2,c:4'], ['b:5,a:1', 'a:1,b:5'], ['a:-2,a:-3', 'a:-5'], ['k:100,j:7,k:23', 'j:7,k:123'], ['z:1,y:2', 'y:2,z:1']]


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
