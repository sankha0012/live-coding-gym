Write a Python 3.12 function clean_events(events) using only the standard library.
- Input: a list of dicts with keys "event_id" (str), "ts" (int, epoch seconds) and "payload" (dict). Output: a new list of dicts.
- Two events with the same event_id are duplicates. Keep only the one with the highest ts. If the ts is equal, keep the one that appeared first in the input.
- Return the kept events sorted by ts ascending. Break ties by event_id, so the output is fully deterministic.
- Do not modify the input list or its dicts.
- Edge cases: an empty list returns an empty list. An event missing event_id or ts, or with a ts that is not an int (a bool does not count) or an event_id that is not a str, must raise ValueError that names the position of the bad event.
- It should run in O(n log n) time. Do not use nested loops over the whole list.
Also write pytest tests for: no duplicates, exact duplicates, duplicates with different ts, equal ts ties, unsorted input, empty input and a malformed event. Then explain the complexity and the tie-break rules in a few sentences.
