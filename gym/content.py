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
    seed: str = ""
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
    serves: list = field(default_factory=list)   # competencies C1..C10 from the recruiter email
    docs: str = ""                # documentation page the learner may consult (docs.md)
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
    control: bool = True          # False: no evaluation after the tests pass (tiny test fixtures)
    level: int = 0                # 1 to 3: how much evaluation (reading: yaml `level`; builds: derived from the solution size unless set)
    whatif: list = field(default_factory=list)     # read kind: authored one-line changes with their real outcome
    fix: str = ""                 # read kind, level 3: the "change it so it prints ..." task
    fix_expected: str = ""
    fix_solution: str = ""

    @property
    def control_level(self):
        """Evaluation after a core build passes. 0: none. 1: What if. 2: What if, then a change by hand.
        3: explain two of your lines, then a change by hand."""
        if not self.control or self.kind not in ("python", "sql") or not self.required or self.name_bug or self.assistant == "off":
            return 0
        if self.level:
            return self.level
        size = len([l for l in self.solution.splitlines() if l.strip() and not l.strip().startswith(("#", "--"))])
        return 1 if size <= 10 else 2 if size <= 20 else 3


@dataclass
class Step:
    id: str
    title: str
    order: int
    min_score: int = 3
    pass_ratio: float = 0.7
    lessons: list = field(default_factory=list)
    exercises: list = field(default_factory=list)
    cards: list = field(default_factory=list)
    optional: bool = False        # always open, never blocks the next step, not part of readiness
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
        serves=meta.get("serves") or [],
        level=meta.get("level", 0),
        control=meta.get("control", True),
        docs=_read(d / "docs.md"),
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
        if kind == "sql":  # the changed query is compared with change_solution.sql on the exercise's data
            ex.change_solution = (d / "change_solution.sql").read_text()
        else:
            if not (ex.change_dir / "test_change.py").exists():
                raise ValueError("change.md needs change_tests/test_change.py")
            ex.change_solution = (d / "change_solution.py").read_text()
    ext = EXT.get(kind)
    if ext:
        ex.starter = _read(d / f"starter.{ext}")
        ex.solution = (d / f"solution.{ext}").read_text()
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
        ex.level = ex.level or 2
        ex.whatif = yaml.safe_load(_read(d / "whatif.yaml")) or []
        for i, v in enumerate(ex.whatif, 1):
            if v.get("answer") not in ("same", "different", "crash") or not v.get("change") or "old" not in v or "new" not in v:
                raise ValueError(f"whatif {i}: needs change, old, new and answer: same|different|crash")
        ex.fix, ex.fix_expected, ex.fix_solution = (_read(d / "fix.md"), _read(d / "fix_expected.txt"), _read(d / "fix_solution.py"))
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
            cards=yaml.safe_load(_read(sd / "cards.yaml")) or [],
            optional=meta.get("optional", False),
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
    for step in steps:
        rank = {xid: i for i, xid in enumerate(step.sequence)}
        step.exercises.sort(key=lambda e: (rank.get(e.id, 10_000), e.order, e.id))
        for xid in step.sequence:
            if xid not in {e.id for e in step.exercises}:
                errors.append(f"{step.id}: sequence names unknown exercise {xid}")
    steps.sort(key=lambda s: s.order)
    return steps, errors
