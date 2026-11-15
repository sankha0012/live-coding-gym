import subprocess
import sys

import pytest

CASES = [['The cat and the hat.', 'the'], ['b a b a', 'a'], ['Hello', 'hello'], ['Dog dog, DOG! cat cat', 'dog'], ['zebra apple zebra apple mango', 'apple'], ['c b a', 'a'], ['Apple banana APPLE; banana! cherry', 'apple'], ['b B a A', 'a'], ['x, y. y! x? z', 'x'], ['1 2 2', '2'], ['Go go GO stop', 'go'], ['a b b c c', 'b'], ['Hello, hello. world', 'hello'], ['It is it. IT IS!', 'it']]


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
