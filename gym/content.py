from dataclasses import dataclass, field
from pathlib import Path

import yaml

KINDS = {"python", "sql", "open", "prompt", "explain", "quiz", "tests", "read", "triage"}
ASSISTANTS = ("train", "explain", "off", "free")
EXT = {"python": "py", "sql": "sql", "tests": "py"}


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
    hint: str = ""
    say: str = ""
    model_prompt: str = ""
    guide: str = ""
    files: list = field(default_factory=list)
    wrong: dict = field(default_factory=dict)
    alt: dict = field(default_factory=dict)
    quiz: list = field(default_factory=list)
    pass_ratio: float = 0.8
    order: int = 50
    kb: list = field(default_factory=list)
    impl_good: str = ""
    impls_bad: dict = field(default_factory=dict)
    assistant: str = "train"      # train | explain | off | free: what the assistant may do on this exercise
    plan_required: int = 0        # at least this many comment lines (the plan) in a submission
    grade_prompts: bool = False   # the learner's prompts to the assistant must pass the prompt review
    name_bug: bool = False        # the learner must name the bug in one sentence (reviewed against bug.md)
    bug: str = ""
    change: str = ""              # control check: the small change to make by hand
    change_dir: Path | None = None
    change_solution: str = ""
    snippet: str = ""             # read kind: the code to read
    expected: str = ""            # read kind: what it prints
    questions: list = field(default_factory=list)
    proposals: list = field(default_factory=list)  # triage kind


@dataclass
class Step:
    id: str
    title: str
    order: int
    min_score: int = 3
    pass_ratio: float = 0.7
    timed_required: bool = False
    lessons: list = field(default_factory=list)
    exercises: list = field(default_factory=list)
    cards: list = field(default_factory=list)
    shelf: bool = False           # Library step: always unlocked, never gates anything
    includes: list = field(default_factory=list)   # ids of exercises moved into this step from other steps
    sequence: list = field(default_factory=list)   # explicit exercise order
    intro: str = ""


def _read(path):
    return path.read_text() if path.exists() else ""


def _rubric(items):
    """Rubric criteria as plain strings. YAML reads an unquoted `Names a risk: text` as a one-key mapping."""
    return [i if isinstance(i, str) else "; ".join(f"{k}: {v}" for k, v in i.items()) for i in items or []]


def _existing(path):
    if not path.exists():
        raise ValueError(f"file not found: {path}")
    return path


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
        rubric=_rubric(meta.get("rubric")),
        hint=_read(d / "hint.md"),
        say=_read(d / "say.md"),
        model_prompt=_read(d / "model_prompt.md"),
        guide=_read(d / "guide.md"),
        pass_ratio=meta.get("pass_ratio", 0.8),
        order=meta.get("order", 50),
        kb=meta.get("kb") or [],
        files=[_existing((d / f).resolve()) for f in meta.get("files", [])],
        plan_required=meta.get("plan_required", 0),
        grade_prompts=meta.get("grade_prompts", False),
        name_bug=meta.get("name_bug", False),
        bug=_read(d / "bug.md"),
        change=_read(d / "change.md"),
        questions=meta.get("questions") or [],
    )
    policy = meta.get("assistant")
    if policy is False:  # YAML reads an unquoted `off` as a boolean
        policy = "off"
    ex.assistant = policy or ("train" if kind in ("python", "sql", "tests") else "explain")
    if ex.assistant not in ASSISTANTS:
        raise ValueError(f"unknown assistant policy {ex.assistant!r}")
    if ex.name_bug and not ex.bug:
        raise ValueError("name_bug needs bug.md")
    if ex.change:
        ex.change_dir = d / "change_tests"
        if not (ex.change_dir / "test_change.py").exists():
            raise ValueError("change.md needs change_tests/test_change.py")
        ex.change_solution = (d / "change_solution.py").read_text()
    ext = EXT.get(kind)
    if ext:
        ex.starter = _read(d / f"starter.{ext}")
        ex.solution = (d / f"solution.{ext}").read_text()
        ex.gaps = _read(d / f"gaps.{ext}")
    if kind == "python":
        if not (d / "tests" / "test_hidden.py").exists():
            raise ValueError("missing tests/test_hidden.py")
        ex.wrong = {p.stem: p.read_text() for p in sorted((d / "wrong").glob("*.py"))}
    if kind == "sql":
        seed = d / meta["seed_file"] if "seed_file" in meta else d / "seed.sql"
        ex.seed = _existing(seed.resolve()).read_text()
        extra = d / "seed_extra.sql"  # edge-case rows (ties, NULLs, duplicates) added on top of the shared data
        if extra.exists():
            ex.seed += "\n" + extra.read_text()
        ex.wrong = {p.stem: p.read_text() for p in sorted((d / "wrong").glob("*.sql"))}
        ex.alt = {p.stem: p.read_text() for p in sorted((d / "alt").glob("*.sql"))}
    if kind == "tests":
        ex.impl_good = (d / "impl_good.py").read_text()
        ex.impls_bad = {p.stem: p.read_text() for p in sorted(d.glob("impl_bad_*.py"))}
        if not ex.impls_bad:
            raise ValueError("a tests exercise needs at least one impl_bad_*.py")
    if kind == "read":
        ex.snippet = (d / "snippet.py").read_text()
        ex.expected = (d / "expected.txt").read_text()
    if kind == "triage":
        ex.proposals = yaml.safe_load((d / "proposals.yaml").read_text())
        for i, p in enumerate(ex.proposals, 1):
            if p.get("correct") not in ("accept", "reject") or not p.get("title") or not p.get("code"):
                raise ValueError(f"proposal {i}: needs title, code and correct: accept|reject")
    if kind == "quiz":
        ex.quiz = yaml.safe_load((d / "quiz.yaml").read_text())
        for i, q in enumerate(ex.quiz, 1):
            if not 0 <= q["answer"] < len(q["options"]):
                raise ValueError(f"quiz question {i}: answer out of range")
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
            min_score=gate.get("min_score", 3),
            pass_ratio=gate.get("pass_ratio", 0.7),
            timed_required=gate.get("timed_required", False),
            cards=yaml.safe_load(_read(sd / "cards.yaml")) or [],
            shelf=meta.get("shelf", False),
            includes=meta.get("includes") or [],
            sequence=meta.get("sequence") or [],
            intro=meta.get("intro", ""),
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
    # includes: exercises are moved (in the view only; their files stay where they are) into the including step
    home = {ex.id: (s, ex) for s in steps for ex in s.exercises}
    for step in steps:
        for xid in step.includes:
            if xid not in home:
                errors.append(f"{step.id}: includes unknown exercise {xid}")
                continue
            old, ex = home[xid]
            if old is not step:
                old.exercises.remove(ex)
                ex.step_id = step.id
                step.exercises.append(ex)
                home[xid] = (step, ex)
    for step in steps:
        rank = {xid: i for i, xid in enumerate(step.sequence)}
        step.exercises.sort(key=lambda e: (rank.get(e.id, 10_000), e.order, e.id))
        for xid in step.sequence:
            if xid not in {e.id for e in step.exercises}:
                errors.append(f"{step.id}: sequence names unknown exercise {xid}")
    steps.sort(key=lambda s: s.order)
    return steps, errors
