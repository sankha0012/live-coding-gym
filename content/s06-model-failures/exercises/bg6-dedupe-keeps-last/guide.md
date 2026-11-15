**Why this matters.** Retries deliver the same event again, often with a changed field. The pipeline must act on the first delivery, so the choice of which copy survives is part of correctness.

**How we get there.**
1. Run the tests. The first-wins test fails.
2. Reproduce: `dedupe_events([{"id": 1, "v": "a"}, {"id": 1, "v": "b"}])`. It returns the event with `v == "b"`, and the count is 1.
3. Read the loop: `by_id[event["id"]] = event` runs for every event, so a later one replaces an earlier one.
4. Fix: keep a `seen` set. If the id is in `seen`, continue; otherwise add it and append the event to the result list.
5. Return `unique, len(events) - len(unique)`. Run the tests again. All pass.

**Check it.** The duplicate count was right the whole time, so a test on the count alone would not have found this.

**Next time.** When code overwrites by key, ask whether first or last should win and say it aloud.

**Watch out.** `dict.setdefault` also keeps the first and is a valid alternative, as long as the order of the result stays the order of first appearance.
