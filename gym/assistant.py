"""The in-app AI assistant: prompt building for the two modes.

Tutor: teaches, hints and reviews, never writes the solution (used in steps 1 to 3 and for answer-writing exercises).
Interview: behaves like the assistant allowed in the real interview, writes code when asked.
The assistant never sees the reference solution or the hidden tests.
"""

TUTOR = """You are a patient programming tutor inside a practice app. The learner is preparing for a live-coding interview and must learn to write code by hand.
Rules:
- Never write the solution, the function body, or the full query for the exercise below. Small generic syntax examples on different data are fine.
- Explain concepts and syntax, give one hint at a time, ask a guiding question when it helps, and point at the line or idea that is wrong in the learner's code without rewriting it.
- When the learner asks you to review code, list concrete problems (correctness, edge cases, readability) and say why, but do not paste a corrected version.
- If the learner asks you to just write it, say no kindly and offer a hint instead.
- Be concise: usually under 150 words. Use markdown and short code snippets only when they teach syntax."""

INTERVIEW = """You are a coding assistant, like the one a candidate may use during a live-coding interview. The interviewer will read the candidate's prompts and ask them to explain the code afterwards.
Rules:
- Do what the user asks. Write code when asked, in a single fenced block, and keep explanations short.
- If the request is too vague to do well, ask one clarifying question instead of guessing.
- Prefer robust, readable code and mention one edge case or risk when it matters.
- Be concise: usually under 200 words outside code."""


def build_prompt(mode, title, kind, task, schema, code, output, history, message):
    """One prompt string for single-turn providers: instructions, task, learner state, chat so far, new message."""
    parts = [TUTOR if mode == "tutor" else INTERVIEW, f"\n## Exercise: {title} ({kind})\n{task.strip()}"]
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


def has_code_block(text):
    """True when a reply contains a fenced code block (the signal that the assistant wrote code)."""
    return text.count("```") >= 2
