**Why this matters.** JSON is how programs talk to each other. Two details decide whether it works in practice: output that is the same every time, and input that may be garbage.

**How we get there.**
1. To write JSON, call `json.dumps(data)`. By default the key order follows the dict and there are spaces after commas and colons.
2. Pass `sort_keys=True`. Keys are then sorted at every level, so equal data always gives equal text.
3. Pass `separators=(",", ":")` to drop the spaces and make the text compact.
4. To read JSON, call `json.loads(text)`. Bad text raises `json.JSONDecodeError`, and the empty string counts as bad text.
5. Wrap that call in `try` and catch `json.JSONDecodeError`, returning `None`.

**Check it.** Writing then reading gives back the original data. Both directions are linear in the size of the data.

**Watch out.** Catching a bare `Exception` would hide real bugs. We catch only the one error we expect. Returning `None` also hides why parsing failed, which real code would log.
