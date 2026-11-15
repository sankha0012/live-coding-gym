Write apply_events(events). Each event has event_id, order_id, ts and status. Events can be duplicated (same event_id) and arrive out of order. Return ({order_id: status of the latest event}, number of duplicates skipped). If two different events have the same ts, the larger event_id wins.

*Feature store updates from a stream that delivers at-least-once.*
