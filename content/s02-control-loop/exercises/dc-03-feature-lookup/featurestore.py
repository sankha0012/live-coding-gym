"""Tiny in-memory feature store with one numeric feature per entity."""

_STORE = {"u1": 0.5, "u2": 0.0, "u3": 12.0, "u4": 3.5}
_UNSET = object()


def get_features(keys, *, default=_UNSET):
    """Return {key: value} for the entities in keys; see docs.md for absent keys."""
    out = {}
    for k in keys:
        if k in _STORE:
            out[k] = _STORE[k]
        elif default is not _UNSET:
            out[k] = default
    return out
