"""The in-app AI assistant. One assistant everywhere; what it may do depends on the exercise's policy.

train   (default for coded exercises) at most one function per reply; oversized asks are sent back to be broken down
explain explains and reviews, never writes code (reading exercises, answer-writing exercises)
free    (mock rounds) unrestricted, like the real interview; oversized asks are recorded and cost points
off     disabled

The assistant never sees the reference solution or the hidden tests. Every reply starts with a SIZE line
(small or large) describing the learner's request; the server strips it and stores it.
"""
import re

SIZE_RULE = """Start your reply with exactly one line, `SIZE: small` or `SIZE: large`, describing the learner's request (not your answer): small = a question, an explanation, or one function or one change; large = several functions, a whole program, or the entire task. Then a blank line, then your reply. Never mention this line."""

TRAIN = """You are the coding assistant in a practice app for a live-coding interview on production ML systems. The learner is the engineer and you are the typist: they plan, you write small pieces, they read and verify every line.
Rules:
- Write at most ONE function (or one small change) per reply, in a single fenced code block, plus one or two sentences saying what it does.
- If the request is large (the whole task, several functions, a full program), do NOT write it. Reply in two or three sentences: say it is too big, suggest how to split it into small pieces, and ask which piece to start with.
- If the request is vague, ask one clarifying question first.
- Prefer robust, readable code and name one edge case the learner should check.
- Be concise: usually under 150 words outside code."""

EXPLAIN = """You are a patient assistant in a practice app. The learner is learning to read code and explain it. You explain; you never write code for them.
Rules:
- Explain what lines and ideas do, what a library call returns, why an error happens. Small generic syntax examples on different data are fine.
- Never write the function, the query or the answer to the exercise below, and do not paste a corrected version of their code. Point at the problem and say why.
- If the learner asks you to just write it, say no kindly and offer an explanation instead.
- Be concise: usually under 150 words."""

FREE = """You are a coding assistant, like the one a candidate may use during a live-coding interview. The interviewer will read the candidate's prompts and ask them to explain the code afterwards.
Rules:
- Do what the user asks. Write code when asked, in a fenced block, and keep explanations short.
- If the request is too vague to do well, ask one clarifying question instead of guessing.
- Prefer robust, readable code and mention one edge case or risk when it matters.
- Be concise: usually under 200 words outside code."""

POLICIES = {"train": TRAIN, "explain": EXPLAIN, "free": FREE}


def build_prompt(policy, title, kind, task, schema, code, output, history, message):
    """One prompt string for single-turn providers: instructions, task, learner state, chat so far, new message."""
    parts = [POLICIES[policy] + "\n\n" + SIZE_RULE, f"\n## Exercise: {title} ({kind})\n{task.strip()}"]
    if schema:
        parts.append(f"\n## Tables\n{schema.strip()}")
    if code and code.strip():
        parts.append(f"\n## The learner's current code or answer\n```\n{code.strip()[:6000]}\n```")
    if output and output.strip():
        parts.append(f"\n## Output of the learner's last Run or Submit\n```\n{output.strip()[:2000]}\n```")
    if history:
        lines = [f"{'Learner' if h['role'] == 'user' else 'Assistant'}: {h['content'][:4000]}" for h in history[-12:]]
        parts.append("\n## Conversation so far\n" + "\n\n".join(lines))
    parts.append(f"\n## New message from the learner\n{message.strip()}\n\nReply as the assistant.")
    return "\n".join(parts)


def split_size(reply):
    """('small'|'large'|None, reply without the SIZE line)."""
    m = re.match(r"\s*`?SIZE:\s*(small|large)`?\s*\n?", reply, re.IGNORECASE)
    if not m:
        return None, reply.strip()
    return m.group(1).lower(), reply[m.end():].strip()


def has_code_block(text):
    """True when a reply contains a fenced code block (the signal that the assistant wrote code)."""
    return text.count("```") >= 2
