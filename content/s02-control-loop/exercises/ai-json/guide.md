**Why this matters.** Models wrap their JSON in friendly prose or code fences, so `json.loads` on the whole reply fails. We find the object inside the noise, and cope when there is none.

**How we get there.**
1. Find the first `{` with `text.find("{")` and the last `}` with `text.rfind("}")`. Chatter and fence markers fall outside that span.
2. Reject the no-object cases: a brace is missing (`find` and `rfind` return `-1`), or the closing brace is not after the opening one.
3. Slice `text[start:end + 1]`. The `+ 1` keeps the final brace, since a slice stops before its end index.
4. Pass the slice to `json.loads` inside `try`. Invalid JSON raises a `ValueError` subclass, and we return `None`.

**Check it.** Nested braces are fine, because we take the first opening and last closing brace. Two separate objects in one reply give an invalid slice and `None`. Cost is linear.

**Watch out.** Skipping the `try` crashes on braces that are not JSON, and slicing to `end` drops the last brace.
