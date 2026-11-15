**Why this matters.** A default argument looks fresh on every call, but Python builds it once, when the function is defined. A list there is shared by all calls that use it.

**How we get there.**
1. Reproduce. Call `record_event("a")` and then `record_event("b")` without a list. The second returns `["a", "b"]`, but should be `["b"]`.
2. Locate it: `log=[]` in the signature. That one list lives on the function and keeps growing.
3. Change the default to `log=None`. `None` is immutable, so sharing it is harmless.
4. Inside, create the list when needed: `if log is None: log = []`. Each call without a list gets its own.
5. Append and return as before. A list the caller passes is still appended to in place and returned as the same object.

**Check it.** We test `is None`, not `if not log`. An empty list from the caller is falsy, and replacing it would break the in-place promise.

**Next time.** In AI-written code, treat any `=[]`, `={}` or `=set()` in a signature as a red flag.

**Watch out.** Copying the caller's list fixes the sharing but breaks the in-place contract.
