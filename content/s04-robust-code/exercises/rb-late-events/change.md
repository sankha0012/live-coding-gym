Change: deleted entities disappear. If the winning event of an entity (the one that wins after removing duplicates and applying the tie rule) has `state == "deleted"`, leave that entity out of the result.

For example, `[{"id": "1", "entity": "a", "ts": 1, "state": "new"}, {"id": "2", "entity": "a", "ts": 2, "state": "deleted"}]` gives `{}`. A `"deleted"` event that is older than another event of the same entity does not remove it: only the winning event counts, so an entity that is deleted and then created again at a later `ts` stays in the result. The state `"deleted"` is not special for anything else.

Do this by hand in your own passing solution. It should take one or two lines.
