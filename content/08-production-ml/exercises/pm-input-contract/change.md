Add an optional `"choices"` rule. A rule may now contain `"choices"`, a list of allowed values, for example `{"type": str, "choices": ["free", "pro"]}`.

- The type check still comes first: a value of the wrong type adds `"bad_type:<field>"` as before.
- A value of the right type that is not in `choices` adds `"bad_choice:<field>"` and the field is left out of `clean`.
- A value that is in `choices` passes (and then the usual `min` and `max` checks still apply).
- A missing or `None` field is handled as before; `choices` is not checked for it.
- A rule without `"choices"` behaves exactly as before.

Example with `{"plan": {"type": str, "choices": ["free", "pro"]}}`: `{"plan": "gold"}` gives `({}, ["bad_choice:plan"])`, `{"plan": "pro"}` gives `({"plan": "pro"}, [])` and `{"plan": 3}` gives `({}, ["bad_type:plan"])`.
