Change: a force list. Add an optional last parameter `force_canary=()` to `assign_arm`, so the signature is `assign_arm(user_id, canary_percent=5, salt="canary-v1", force_canary=())`.

It is a collection of user ids (a tuple, list or set). A user whose id is in `force_canary` always gets `"canary"`, even when `canary_percent` is `0`. Every other user is assigned exactly as before. For example, `assign_arm("qa-1", 0, force_canary={"qa-1"})` returns `"canary"`, and `assign_arm("u7", 0, force_canary={"qa-1"})` returns `"stable"`.

Do this by hand in your own passing solution. It should take two lines.
