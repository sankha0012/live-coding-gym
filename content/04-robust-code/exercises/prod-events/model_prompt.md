Write apply_events(events) in Python. Each event is a dict with event_id, order_id, ts, status.
Events may be duplicated (same event_id) and arrive in any order.
Return (state, duplicates) where state maps order_id -> status of the event with the largest (ts, event_id),
and duplicates counts skipped repeats. The result must be the same whatever the input order.
Add asserts: a duplicated event, out-of-order events, a timestamp tie, and the reversed input giving the same result.
