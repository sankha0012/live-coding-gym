from dataclasses import dataclass, field
from pathlib import Path

import yaml

KINDS = {"python", "sql", "open", "prompt", "explain"}
EXT = {"python": "py", "sql": "sql"}


@dataclass
class Exercise:
    id: str
    step_id: str
    title: str
    kind: str
    prompt: str
    dir: Path
    starter: str = ""
    solution: str = ""
    gaps: str = ""
    seed: str = ""
    time_limit_s: int = 600
    required: bool = True
    review: bool = False
    mock: bool = False
    ordered: bool = False
    rubric: list = field(default_factory=list)


@dataclass
class Step:
    id: str
    title: str
    order: int
    min_score: int = 4
    timed_required: bool = False
    lessons: list = field(default_factory=list)
    exercises: list = field(default_factory=list)
    cards: list = field(default_factory=list)


def _read(path):
    return path.read_text() if path.exists() else ""


def load_exercise(d, step_id):
    meta = yaml.safe_load((d / "exercise.yaml").read_text())
    kind = meta["kind"]
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    ex = Exercise(
        id=d.name,
        step_id=step_id,
        title=meta["title"],
        kind=kind,
        prompt=(d / "prompt.md").read_text(),
        dir=d,
        time_limit_s=meta.get("time_limit_s", 600),
        required=meta.get("required", True),
        review=meta.get("review", False),
        mock=meta.get("mock", False),
        ordered=meta.get("ordered", False),
        rubric=meta.get("rubric") or [],
    )
    ext = EXT.get(kind)
    if ext:
        ex.starter = _read(d / f"starter.{ext}")
        ex.solution = (d / f"solution.{ext}").read_text()
        ex.gaps = _read(d / f"gaps.{ext}")
    if kind == "python" and not (d / "tests" / "test_hidden.py").exists():
        raise ValueError("missing tests/test_hidden.py")
    if kind == "sql":
        ex.seed = (d / "seed.sql").read_text()
    return ex


def load_content(content_dir):
    steps, errors = [], []
    content_dir = Path(content_dir)
    if not content_dir.exists():
        return steps, [f"content directory not found: {content_dir}"]
    for sd in sorted(p for p in content_dir.iterdir() if (p / "step.yaml").exists()):
        meta = yaml.safe_load((sd / "step.yaml").read_text())
        gate = meta.get("gate") or {}
        step = Step(
            id=sd.name,
            title=meta["title"],
            order=meta["order"],
            min_score=gate.get("min_score", 4),
            timed_required=gate.get("timed_required", False),
            cards=yaml.safe_load(_read(sd / "cards.yaml")) or [],
        )
        for lp in sorted((sd / "lessons").glob("*.md")):
            body = lp.read_text()
            title = body.splitlines()[0].lstrip("# ").strip() if body.strip() else lp.stem
            step.lessons.append({"id": lp.stem, "title": title, "body": body})
        ex_root = sd / "exercises"
        for ed in sorted(p for p in ex_root.iterdir() if p.is_dir()) if ex_root.exists() else []:
            try:
                step.exercises.append(load_exercise(ed, sd.name))
            except Exception as e:  # one broken exercise must not stop the app
                errors.append(f"{ed}: {e}")
        steps.append(step)
    steps.sort(key=lambda s: s.order)
    return steps, errors
