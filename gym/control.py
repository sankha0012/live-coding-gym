"""The control check: pick two lines of the learner's own code to explain."""
import random
import re

SKIP = re.compile(r"^(#|import |from |@|\"\"\"|'''|else:|try:|finally:|pass$|return$|\)|\]|\})")


def candidate_lines(code):
    """(line number, text) of lines worth asking about: real logic, not comments, imports or punctuation."""
    out = []
    for no, text in enumerate(code.splitlines(), 1):
        s = text.strip()
        if len(s) >= 10 and not SKIP.match(s):
            out.append((no, text.rstrip()))
    return out


def pick_lines(code, seed, n=2):
    """Two lines, in file order, chosen at random but fixed for a given seed (the attempt id)."""
    lines = candidate_lines(code)
    if len(lines) < n:  # tiny solution: fall back to any non-empty lines
        lines = [(no, t.rstrip()) for no, t in enumerate(code.splitlines(), 1) if t.strip()]
    chosen = sorted(random.Random(seed).sample(lines, min(n, len(lines))))
    return [{"no": no, "text": text} for no, text in chosen]
