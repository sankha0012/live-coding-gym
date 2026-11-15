Write `is_rate_limited(timestamps, now, window, limit)` for a rate limiter. `timestamps` holds the times (in seconds) of earlier requests, `now` is the time of the new request, `window` is the window length in seconds, and `limit` is the number of requests allowed per window.

Return `True` when the new request must be rejected, that is, when `limit` or more earlier requests happened in the last `window` seconds before `now`. The window covers the `window` seconds that end at `now`, and a request made exactly at `now` is not an earlier request.

Use the `eventwin` helper for the counting. Documentation is available below the task, consult it. Check the bounds in the docs before you write the call.
