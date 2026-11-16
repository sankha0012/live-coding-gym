"""What if: change one line of some code and ask whether it still works.

Builds: the learner's own passing code is changed, and the hidden tests (or the reference query result) judge the
change. Readings: authored changes in whatif.yaml are judged by running the snippet. Answers always come from a real run.
"""
import random
import re

# (pattern, replacement, what it does): applied to the code part of a line, never inside a string
SWAPS = [(r"<=", "<"), (r">=", ">"), (r"==", "!="), (r"!=", "=="), (r"(?<![<>=!])<(?!=)", "<="), (r"(?<![<>=!-])>(?!=)", ">="),
         (r" \+ ", " - "), (r" - ", " + "), (r" and ", " or "), (r" or ", " and "), (r"\bnot ", ""), (r"\bTrue\b", "False"),
         (r"\bFalse\b", "True"), (r"\bDESC\b", "ASC"), (r"\bASC\b", "DESC"), (r"\bLEFT JOIN\b", "INNER JOIN"),
         (r"\bINNER JOIN\b", "LEFT JOIN"), (r"\bUNION ALL\b", "UNION")]
NUMBER = re.compile(r"(?<![\w.'\"])\d+(?![\w.'\"])")
KEYWORD = re.compile(r"^\s*(def|class|if|elif|else|for|while|try|except|finally|with|return|import|from|@|\)|\]|\}|SELECT|FROM|WHERE|GROUP|ORDER|HAVING|JOIN|LEFT|INNER|ON|AND|OR|WITH|LIMIT|UNION)\b", re.I)
COMMENT = re.compile(r"^\s*(#|--)")


def _in_string(text, pos):
    before = text[:pos]
    return before.count("'") % 2 == 1 or before.count('"') % 2 == 1


def candidates(code, sql=False):
    """Every one-line change: swap an operator, bump a number, or delete a simple statement."""
    out = []
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if not line.strip() or COMMENT.match(line):
            continue
        for pat, rep in SWAPS:
            for m in re.finditer(pat, line, re.I if sql else 0):
                if not _in_string(line, m.start()):
                    out.append((i, line[:m.start()] + rep + line[m.end():]))
        for m in NUMBER.finditer(line):
            if not _in_string(line, m.start()):
                out.append((i, line[:m.start()] + str(int(m.group()) + 1) + line[m.end():]))
        simple = not sql and not KEYWORD.match(line) and not line.rstrip().endswith((":", "(", ",", "\\")) \
            and line.count("(") == line.count(")") and line.count("[") == line.count("]")
        if simple:
            out.append((i, line[:len(line) - len(line.lstrip())] + "pass"))
    mutants = []
    for i, new in out:
        if new != lines[i]:
            mutants.append({"line": i + 1, "old": lines[i].strip(), "new": new.strip(),
                            "code": "\n".join(lines[:i] + [new] + lines[i + 1:])})
    return mutants


def describe(m):
    if m["new"] == "pass":
        return f"Line {m['line']}: `{m['old']}` is deleted."
    return f"Line {m['line']}: `{m['old']}` becomes `{m['new']}`."


def valid_python(code):
    import ast
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def pick(code, seed, judge, want=3, sql=False, limit=6):
    """Change the code `want` ways. judge(changed_code) -> 'pass' or 'fail' by really running it. The set has both
    outcomes when the code allows it. Returns [{'change', 'answer'}]."""
    pool = [m for m in candidates(code, sql) if sql or valid_python(m["code"])]
    random.Random(seed).shuffle(pool)
    seen, found = set(), []
    for m in pool:
        if len(found) >= limit or ({a for _, a in found} >= {"pass", "fail"} and len(found) >= want):
            break
        key = (m["line"], m["new"])
        if key in seen:
            continue
        seen.add(key)
        found.append((m, judge(m["code"])))
    chosen = []
    for outcome in ("fail", "pass"):  # at least one of each, then fill up
        hit = next((x for x in found if x[1] == outcome and x not in chosen), None)
        if hit:
            chosen.append(hit)
    chosen += [x for x in found if x not in chosen][:max(0, want - len(chosen))]
    random.Random(seed + 1).shuffle(chosen)
    return [{"change": describe(m), "answer": a} for m, a in chosen[:want]]
