Events from a message queue arrive late, out of order, and sometimes twice. Rebuild the current state of each entity.

Write `final_state(events) -> dict`. Each event is a dict `{"id": str, "entity": str, "ts": int, "state": str}`. Return a dict mapping each entity to the `state` of its event with the highest `ts`.

- Events with the same `id` are duplicates of one event: keep only the first one that appears in the list and ignore the others.
- After removing duplicates, if two events of the same entity have the same `ts`, the one that appears later in the list wins.
- Do not modify the input. An empty list returns `{}`.
