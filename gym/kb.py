"""The in-app knowledge base: short reference articles under content/_kb/<topic-id>.md.

An article starts with YAML front matter (title, summary, tags). The text before the
`<!-- more -->` marker is the brief shown in the exercise sidebar; the whole text is the article.
"""
from dataclasses import dataclass
from pathlib import Path

import yaml

MORE = "<!-- more -->"


@dataclass
class Topic:
    id: str
    title: str
    summary: str
    tags: list
    brief: str
    body: str


def load_kb(content_dir):
    topics, errors = {}, []
    root = Path(content_dir) / "_kb"
    for path in sorted(root.glob("*.md")) if root.exists() else []:
        try:
            _, front, text = path.read_text().split("---", 2)
            meta = yaml.safe_load(front)
            brief, _, rest = text.partition(MORE)
            if not brief.strip():
                raise ValueError("empty brief (text before <!-- more -->)")
            topics[path.stem] = Topic(path.stem, meta["title"], meta["summary"], meta.get("tags") or [],
                                      brief.strip(), (brief + rest).strip())
        except Exception as e:  # one broken article must not stop the app
            errors.append(f"{path}: {e}")
    return topics, errors
