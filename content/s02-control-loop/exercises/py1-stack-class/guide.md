**Why this matters.** A stack is last in, first out: undo history, the call stack, matching brackets. Building one by hand shows how a small class can hide a simple list behind a clean interface.

**How we get there.**
1. In `__init__`, create an empty list `self._items`. The underscore tells readers it is private to the class.
2. `push(x)` is `append`, which adds to the end, the top of the stack.
3. `pop()` removes from the end with the list's own `pop()`. First check for empty and raise `IndexError`, so the caller gets a clear error instead of a confusing one.
4. `peek()` does the same check and then returns `self._items[-1]` without removing it.
5. Add `__len__` returning `len(self._items)`, which makes `len(stack)` work.

**Check it.** Push and pop at the end are constant time. Pushing three items and popping three returns them in reverse order.

**Watch out.** Returning `None` from an empty `pop` is tempting, but a caller cannot tell it from a stored `None`. Popping from the front would also be slow and wrong.
