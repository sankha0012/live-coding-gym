import json
import re

from fastapi.testclient import TestClient

from gym.app import create_app
from gym.check_content import check_kb
from gym.content import load_content
from gym.kb import load_kb

ARTICLE = """---
title: split and join
summary: Split a string into words and join them back.
tags: [python, strings]
---
`s.split()` splits on whitespace.

<!-- more -->

## Details

See also [slicing](#/kb/py-slicing).
"""


def build(tmp_path, kb_line="kb: [py-split]\n"):
    root = tmp_path / "c"
    ex = root / "01-s" / "exercises" / "e1"
    ex.mkdir(parents=True)
    (root / "01-s" / "step.yaml").write_text("title: S\norder: 1\n")
    (ex / "exercise.yaml").write_text("title: E\nkind: open\n" + kb_line)
    (ex / "prompt.md").write_text("p")
    (ex / "say.md").write_text("s")
    (root / "_kb").mkdir()
    (root / "_kb" / "py-split.md").write_text(ARTICLE)
    (root / "_kb" / "py-slicing.md").write_text(ARTICLE.replace("split and join", "slicing").replace("#/kb/py-slicing", "#/kb/py-split"))
    return root


def test_loader_splits_brief_from_body_and_reports_broken_articles(tmp_path):
    root = build(tmp_path)
    (root / "_kb" / "bad.md").write_text("no front matter")
    topics, errors = load_kb(root)
    t = topics["py-split"]
    assert t.title == "split and join" and t.tags == ["python", "strings"]
    assert t.brief == "`s.split()` splits on whitespace." and "## Details" in t.body and t.brief in t.body
    assert len(errors) == 1 and "bad.md" in errors[0]


def test_api_serves_index_article_and_exercise_topics(tmp_path):
    root = build(tmp_path)
    client = TestClient(create_app(root, tmp_path / "p.db", call=lambda p: json.dumps({})))
    assert {t["id"] for t in client.get("/api/kb").json()} == {"py-split", "py-slicing"}
    assert "## Details" in client.get("/api/kb/py-split").json()["body"]
    assert client.get("/api/kb/nope").status_code == 404
    kb = client.get("/api/exercise/e1").json()["kb"]
    assert [t["id"] for t in kb] == ["py-split"] and kb[0]["brief"].startswith("`s.split()`")


def test_checker_reports_unknown_topics_and_broken_links(tmp_path):
    root = build(tmp_path, kb_line="kb: [py-split, py-missing]\n")
    (root / "_kb" / "py-slicing.md").unlink()
    steps, _ = load_content(root)
    problems = check_kb(root, steps)
    assert "e1: unknown kb topic py-missing" in problems
    assert any("link to missing kb topic py-slicing" in p for p in problems) and len(problems) == 2
