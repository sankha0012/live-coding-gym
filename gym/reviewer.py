import json
import os
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

REVIEW_KIND = {"python": "code", "sql": "code", "explain": "explain", "prompt": "prompt", "open": "open"}

DEFAULT_RUBRICS = {
    "code": [
        "Correct, including edge cases the tests may not cover",
        "Readable: clear names and structure",
        "Robust: handles bad or unexpected input sensibly",
        "No unnecessary complexity",
    ],
    "explain": [
        "Accurately describes what the code does, step by step",
        "States trade-offs and complexity",
        "Names failure modes and limits honestly",
        "Clear and concise, as spoken to an interviewer",
    ],
    "prompt": [
        "States the task, inputs, outputs and constraints precisely",
        "Asks for robustness: validation, edge cases, determinism",
        "Keeps the candidate in control: small scope, asks for tests or explanation",
        "Would convince an observer the candidate understands the problem",
    ],
    "open": [
        "Technically accurate",
        "Shows understanding of what problem the tool or idea solves",
        "Gives a concrete example",
        "Honest about limits of own experience",
    ],
    "mock": [
        "Answers the follow-up questions directly and correctly",
        "Explains reasoning and trade-offs behind the code",
        "Identifies what could fail in production",
        "Communicates clearly under pressure",
    ],
}

ROLES = {
    "code": "You are a senior engineer interviewing a candidate for a production ML systems role. Review the candidate's code.",
    "explain": "You are an interviewer. The candidate is explaining their own code after a live-coding exercise. Judge the explanation.",
    "prompt": "You are an interviewer watching a candidate use an AI coding assistant. Judge the prompt the candidate wrote for the assistant.",
    "open": "You are an interviewer for an AI/ML engineering role. Grade the candidate's answer to a theory question.",
    "mock": "You are an interviewer. Grade the candidate's answers to your follow-up questions about their code.",
}

FALLBACK_QUESTIONS = [
    "Walk me through your code line by line. Why did you structure it this way?",
    "What inputs would break this code, and how would you defend against them?",
    "How would this behave in production with 100 times more data, and what would you monitor?",
]


def call_gemini(prompt, timeout=60):
    model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }).encode()
    req = urllib.request.Request(
        API.format(model=model),
        data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _material(material):
    return "\n\n".join(f"## {k.upper()}\n{v}" for k, v in material.items() if v)


def build_prompt(kind, rubric, material):
    criteria = "\n".join(f"- {c}" for c in rubric)
    return (
        f"{ROLES[kind]}\n\n"
        "Score each criterion from 1 (poor) to 5 (excellent). Be strict: 4 means an "
        "interviewer would be satisfied, 5 means impressed.\n\n"
        f"Criteria, in order:\n{criteria}\n\n"
        f"{_material(material)}\n\n"
        f"Return exactly {len(rubric)} scores, in the same order as the criteria, as JSON:\n"
        '{"scores": [int, ...], "verdict": "one sentence", '
        '"feedback": "specific, actionable feedback that quotes the candidate\'s work"}'
    )


def parse_review(text, rubric):
    data = json.loads(text)
    scores = [int(s) for s in data["scores"]]
    if len(scores) != len(rubric) or not all(1 <= s <= 5 for s in scores):
        raise ValueError(f"bad scores: {scores}")
    return {"scores": dict(zip(rubric, scores)), "verdict": str(data["verdict"]),
            "feedback": str(data["feedback"])}


def review(kind, rubric, material, call=call_gemini):
    rubric = rubric or DEFAULT_RUBRICS[kind]
    prompt = build_prompt(kind, rubric, material)
    error = None
    for _ in range(2):
        try:
            return {"status": "done", **parse_review(call(prompt), rubric)}
        except Exception as e:  # network, quota, bad JSON: all end as pending
            error = e
    return {"status": "pending", "scores": {}, "verdict": "",
            "feedback": f"Review unavailable: {error}. Your submission is saved; retry later."}


def followups(task, code, call=call_gemini):
    prompt = (
        "You are an interviewer for a production ML systems role. The candidate just "
        "finished this live-coding task. Ask exactly 3 follow-up questions that probe "
        "whether they understand their own code: design choices, edge cases, and "
        "production behaviour. Refer to specific lines.\n\n"
        f"## TASK\n{task}\n\n## CODE\n{code}\n\n"
        'Return JSON: {"questions": ["...", "...", "..."]}'
    )
    try:
        questions = [str(q) for q in json.loads(call(prompt))["questions"]][:3]
        if len(questions) == 3:
            return questions
    except Exception:
        pass
    return FALLBACK_QUESTIONS
