An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`record_event(event, log=None)` appends `event` to `log` and returns the list. If the caller passes a list, that same list object is appended to in place and returned. If no list is passed, each call starts a new empty list, so two calls without `log` never share events.
