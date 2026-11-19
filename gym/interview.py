"""Written answers as a short exchange with an interviewer: one question at a time, at most one follow-up each.

Verdicts are good, partial or missed (scores 5, 3, 1; a step needs 3). Asking for a hint caps a question at partial,
skipping counts as missed. The reference answer never leaves the server; only the interviewer's short reply and a
two-sentence "what a strong answer sounds like" are shown.
"""
import json

SCORE = {"good": 5, "partial": 3, "missed": 1}
MAX_FOLLOWUPS = 1

ROLE = (
    "You are a friendly but sharp interviewer for a production machine-learning engineering role. "
    "You ask one question at a time and listen to short, spoken-style answers. Two or three sentences are a good answer unless the question itself asks for a longer one; "
    "never ask for an essay and never grade length or polish. Judge only what the question asks."
)


def new_state(questions):
    """Each question is a string, or {"q", "ref"} when it carries its own private notes on a strong answer."""
    items = [q if isinstance(q, dict) else {"q": q} for q in questions]
    return {"qs": [{"q": i["q"], "ref": i.get("ref", ""), "turns": [], "followups": 0, "hinted": False, "verdict": None, "strong": ""}
                   for i in items],
            "done": False, "passed": None}


def current(state):
    return next((i for i, q in enumerate(state["qs"]) if q["verdict"] is None), None)


def _conversation(q):
    lines = [f"Interviewer: {q['q']}"]
    for t in q["turns"]:
        lines.append(("Candidate: " if t["who"] == "you" else "Interviewer: ") + t["text"])
    return "\n".join(lines)


def build_prompt(q, reference, rubric, context, action):
    head = (f"{ROLE}\n\n## Question\n{q['q']}\n\n## What a strong answer covers (private, never quote it)\n{reference or '(judge from the code and the question)'}\n"
            + ("".join(f"- {r}\n" for r in rubric) if rubric else "")
            + (f"\n## Code or data the question is about\n{context}\n" if context else "")
            + f"\n## Conversation so far\n{_conversation(q)}\n")
    if action == "hint":
        return head + '\nThe candidate asks for a hint. Give one short nudge that points at where to look, without giving the answer.\nReturn JSON: {"reply": "one nudge, max 25 words"}'
    final = q["followups"] >= MAX_FOLLOWUPS
    return head + (
        "\n## Your move\n"
        "verdict good: the answer names the core point, even briefly. verdict partial: it is on the right track but vague, or misses the reason or the consequence. verdict missed: it is wrong or empty.\n"
        + ("You have already asked a follow-up, so the verdict must be good, partial or missed.\n" if final else
           'If the answer is not clearly good, return verdict "probe" with ONE follow-up question aimed at the specific gap, one sentence, said as an interviewer would, never revealing the answer.\n')
        + 'reply: one short line (max 25 words) reacting like an interviewer; no scores, no markdown. With a final verdict the reply is a statement, never a question. '
          'strong: only for a final verdict: what a strong answer sounds like, in at most 2 spoken sentences written in the first person as the candidate would say it.\n'
          'Return JSON: {"verdict": "good|partial|missed' + ('' if final else '|probe') + '", "reply": "...", "follow_up": "...", "strong": "..."}')


def parse_move(raw, final):
    data = json.loads(raw)
    verdict = str(data["verdict"]).strip().lower()
    allowed = ("good", "partial", "missed") if final else ("good", "partial", "missed", "probe")
    if verdict not in allowed:
        raise ValueError(f"verdict {verdict!r}")
    follow = str(data.get("follow_up") or "").strip()
    if verdict == "probe" and not follow:
        raise ValueError("probe without a follow-up")
    return {"verdict": verdict, "reply": str(data.get("reply") or "").strip(), "follow_up": follow, "strong": str(data.get("strong") or "").strip()}


def ask(call, q, reference, rubric, context, action, text=""):
    """One AI turn. Returns the parsed move, or raises if the AI cannot answer (the state is then left untouched)."""
    probe = {**q, "turns": q["turns"] + ([{"who": "you", "text": text}] if text else [])}
    prompt = build_prompt(probe, reference, rubric, context, action)
    last = None
    for _ in range(2):
        try:
            raw = call(prompt)
            if action == "hint":
                return {"reply": str(json.loads(raw)["reply"]).strip()}
            return parse_move(raw, q["followups"] >= MAX_FOLLOWUPS)
        except Exception as e:  # network, quota, bad JSON
            last = e
    raise RuntimeError(f"The interviewer could not answer: {last}")


def apply(state, action, text, move):
    """Record one candidate action and the interviewer's move in the state."""
    i = current(state)
    q = state["qs"][i]
    if action == "hint":
        q["hinted"] = True
        q["turns"] += [{"who": "you", "text": "(asked for a hint)"}, {"who": "interviewer", "text": move["reply"]}]
        return state
    if action == "skip":
        q["turns"].append({"who": "you", "text": "(skipped)"})
        q["verdict"], q["strong"] = "missed", move.get("strong", "")
        if move.get("reply"):
            q["turns"].append({"who": "interviewer", "text": move["reply"]})
    else:
        q["turns"].append({"who": "you", "text": text})
        if move["verdict"] == "probe":
            q["followups"] += 1
            q["turns"].append({"who": "interviewer", "text": (move["reply"] + " " + move["follow_up"]).strip()})
        else:
            q["verdict"] = "partial" if q["hinted"] and move["verdict"] == "good" else move["verdict"]
            q["strong"] = move["strong"]
            if move["reply"]:
                q["turns"].append({"who": "interviewer", "text": move["reply"]})
    if current(state) is None:
        state["done"] = True
        state["passed"] = all(x["verdict"] != "missed" for x in state["qs"])
    return state


def skip_move(q, reference):
    """Skipping needs no AI: the strong answer is the reference, trimmed."""
    text = (reference or "").strip()[:400]
    return {"reply": "", "strong": text[:text.rfind(".") + 1] if "." in text else text}


def scores(state):
    return {f"Q{i}: {q['q'][:60]}": SCORE[q["verdict"]] for i, q in enumerate(state["qs"], 1)}


def get_scores(state):
    """The score of each question, in order (what the mock round adds up)."""
    return [SCORE[q["verdict"]] for q in state["qs"]]


QUESTION_TYPES = [
    "Design choice: pick a specific line, quote it with its number, and ask why the candidate chose it and what the obvious alternative would cost.",
    "Behaviour: pick an edge case or bad input for this code (empty, duplicate, missing, malformed, huge). Ask what the code does, and whether that is the right thing to do.",
    "Production: tie the code to the focus below (scale, failure, randomness, bad data, model behaviour). Ask what would go wrong in a real system and how they would find out or prevent it.",
]


def questions_prompt(task, code, focus, n, reference="", avoid=(), number=True):
    numbered = "\n".join(f"{i}: {l}" for i, l in enumerate(code.splitlines(), 1)) if number else code
    kinds = "\n".join(f"{i}. {t}" for i, t in enumerate(QUESTION_TYPES[:n], 1))
    return (f"{ROLE}\n\nThe candidate just passed this live-coding task. Write exactly {n} interview questions about THEIR code, to find out whether they understand it.\n\n"
            f"## Task\n{task}\n\n## The candidate's code (line numbers added)\n{numbered}\n\n"
            + (f"## A reference solution (private)\n{reference}\n\n" if reference else "")
            + f"## Focus of this exercise\n{focus or 'writing reliable Python'}\n\n## Questions, in this order\n{kinds}\n\n"
            "Rules: answerable in two or three spoken sentences; never yes/no; never about tests; never ask what a line does; "
            "never ask for an exact computed output; refer to the candidate's own lines and names.\n"
            + ("Do not repeat or rephrase these earlier questions:\n" + "".join(f"- {q}\n" for q in avoid) if avoid else "")
            + 'For each question also write "strong": private notes, at most 2 sentences, on what a correct answer must say.\n'
              'Return JSON: {"questions": [{"q": "...", "strong": "..."}]}')


def make_questions(call, task, code, focus, n, reference="", avoid=(), number=True):
    """n interview questions about the learner's own code: [{"q", "ref"}]. Raises RuntimeError if the AI cannot write them."""
    prompt = questions_prompt(task, code, focus, n, reference, avoid, number)
    last = None
    for _ in range(2):
        try:
            items = json.loads(call(prompt))["questions"]
            out = [{"q": str(i["q"]).strip(), "ref": str(i.get("strong") or "").strip()} for i in items]
            if len(out) != n or not all(o["q"] for o in out):
                raise ValueError(f"expected {n} questions, got {len(out)}")
            return out
        except Exception as e:  # network, quota, bad JSON, wrong count
            last = e
    raise RuntimeError(f"The interviewer could not write questions: {last}")
