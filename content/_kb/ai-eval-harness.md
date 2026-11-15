---
title: A tiny evaluation harness
summary: Run a model over a fixed list of cases, score each output, and report the mean and the failed case ids.
tags: [ai, evaluation]
---
```python
def evaluate(model, cases, score):
    """cases: list of {"id", "input", "expected"}. score(output, expected) -> 0.0 to 1.0."""
    rows = []
    for case in cases:
        try:
            output = model(case["input"])
            s = score(output, case["expected"])
        except Exception as e:
            output, s = f"error: {type(e).__name__}", 0.0     # a crash is a failed case
        rows.append({"id": case["id"], "output": output, "score": s})
    mean = sum(r["score"] for r in rows) / len(rows) if rows else 0.0
    return {"mean": mean, "failed": [r["id"] for r in rows if r["score"] < 1.0], "rows": rows}
```

- Use it before changing a prompt, a model or a retrieval setting, and again after.
- Key rule: fixed cases, a scoring function, and per-case results, not only one number.
- Say: "Without an eval set a prompt change is a guess. With one it is a measured before and after."

<!-- more -->

## Details

```python
cases = [
    {"id": "c1", "input": "2+2", "expected": "4"},
    {"id": "c2", "input": "3+3", "expected": "6"},
]

def exact(output, expected):
    return float(output.strip() == expected)

report = evaluate(lambda q: " 4 ", cases, exact)
report["mean"], report["failed"]             # (0.5, ['c2'])
evaluate(lambda q: 1 / 0, cases, exact)["rows"][0]["output"]   # 'error: ZeroDivisionError'
evaluate(lambda q: "4", [], exact)["mean"]   # 0.0
```

The model is passed in as a function. In a test it is a fake, so the harness itself is deterministic.

**Scoring functions**, from strict to loose:

- Exact match after normalising (strip, lower-case).
- Contains a required string, or matches a regular expression.
- Valid JSON with the right keys and values.
- A numeric answer within a tolerance.
- A second model as judge. Flexible, but it has its own errors, so check it against human labels.

**The cases.** Start with 20 to 50 real examples. Include edge cases and every bug you have seen, so it cannot come back. Keep a part that you never tune prompts against, for the same reason as a test set in ML.

**Reading the result.** Look at the failed cases, not only the mean. With few cases, a small change in the mean is noise. Run a non-deterministic model several times, or set its temperature to 0.

**Regression gate.** Store the last report. A change that makes a previously passing case fail deserves a look even when the mean went up.

## Common mistakes

- Letting one exception stop the run, so later cases are never scored.
- Dividing by zero on an empty case list.
- Reporting only the mean, so nobody sees which cases broke.
- Tuning the prompt on the same cases used to report the final score.
- Comparing raw strings, so `"4"` and `" 4\n"` count as different answers.

## See also

- [Precision, recall, F1 and accuracy](#/kb/ml-metrics-precision-recall-f1)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
- [Parsing JSON from an LLM reply](#/kb/ai-llm-json-parsing)
