**Why this matters.** A bare `except` that returns a default makes code look robust while hiding every failure. Here a corrupt value like `"abc"` quietly becomes "zero items" and flows into a bill or a model.

**How we get there.**
1. Reproduce. `parse_quantity("abc")` returns `0` when it should be an error, and `"3.5"` does the same.
2. Locate it: `except:` catches everything and returns 0. It even catches the `AttributeError` from `.strip()` on `None`, which is why `None` seemed to work.
3. Handle the legitimate cases explicitly: `if raw is None or raw.strip() == "": return 0`. The `None` check comes first, so `.strip()` is never called on it.
4. For everything else, `return int(raw.strip())` with no `try`. Text that is not a whole number makes `int` raise `ValueError` itself, which is what we want.

**Check it.** `" 7 "` gives 7 after stripping, and `"3.5"` raises because `int` rejects it. Cost is constant.

**Next time.** Search AI-written code for bare `except` or `except Exception` followed by a default return, and ask what it hides.

**Watch out.** Returning `None`, or catching only some errors but still returning 0, keeps the bad data flowing.
