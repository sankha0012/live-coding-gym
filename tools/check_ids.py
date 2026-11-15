"""Check only some content while authoring.

  uv run python -m tools.check_ids ex-id-1 ex-id-2     # run the full checks for those exercises
  uv run python -m tools.check_ids step:03-hand-sql    # lessons and cards of a step load and are well-formed
  uv run python -m tools.check_ids kb                  # knowledge-base articles, their links, and exercise kb ids
"""
import sys

from gym import config
from gym.check_content import check_exercise, check_kb
from gym.content import load_content


def main(args):
    steps, errors = load_content(config.CONTENT_DIR)
    problems, found = [], set()
    ids = {a for a in args if not a.startswith("step:") and a != "kb"}
    if "kb" in args:
        problems += check_kb(config.CONTENT_DIR, steps)
    for s in steps:
        if f"step:{s.id}" in args:
            ids_cards = [c.get("id") for c in s.cards]
            for c in s.cards:
                if not {"id", "front", "back"} <= set(c):
                    problems.append(f"{s.id}: card needs id, front, back: {c}")
            if len(ids_cards) != len(set(ids_cards)):
                problems.append(f"{s.id}: duplicate card ids")
            print(f"{s.id}: {len(s.lessons)} lessons, {len(s.cards)} cards, {len(s.exercises)} exercises")
        for ex in s.exercises:
            if ex.id in ids:
                found.add(ex.id)
                problems += check_exercise(ex)
    problems += [f"{i}: not found or failed to load" for i in sorted(ids - found)]
    problems += [e for e in errors if any(f"/{i}:" in e for i in ids)]
    print("\n".join(problems) if problems else "ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
