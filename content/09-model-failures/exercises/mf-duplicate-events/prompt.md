Event streams deliver the same event more than once after retries. Write `dedupe_events(events)` where `events` is a list of dicts, each with a hashable `"id"` key.

Keep the first event for each id and drop the later ones. The kept events stay in their original order. Return a tuple `(unique, duplicates)` where `unique` is the list of kept events and `duplicates` is the number of events dropped. Two events with the same id are duplicates even if their other fields differ. An empty list returns `([], 0)`. Do not change the input list.
