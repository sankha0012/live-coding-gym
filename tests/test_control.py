from gym.control import candidate_lines, pick_lines

CODE = '''import math

# plan: count words
def count_words(text):
    """Count words."""
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
'''


def test_candidates_skip_comments_imports_and_docstrings():
    texts = [t.strip() for _, t in candidate_lines(CODE)]
    assert "counts = {}" in texts and "counts[word] = counts.get(word, 0) + 1" in texts
    assert not any(t.startswith(("import", "#", '"""')) for t in texts)


def test_two_lines_in_file_order_fixed_per_seed():
    a = pick_lines(CODE, seed=7)
    assert len(a) == 2 and a[0]["no"] < a[1]["no"]
    assert a == pick_lines(CODE, seed=7)
    assert any(pick_lines(CODE, seed=s) != a for s in range(1, 30))  # different attempts, different lines


def test_tiny_code_falls_back_to_any_lines():
    assert [l["text"] for l in pick_lines("x = 1\ny = 2\n", seed=1)] == ["x = 1", "y = 2"]
    assert len(pick_lines("x = 1\n", seed=1)) == 1
