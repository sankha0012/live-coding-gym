import json
import os
import tempfile


def atomic_write_json(path: str, obj) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f)
        os.replace(tmp, path)
    except Exception as e:
        os.unlink(tmp) if os.path.exists(tmp) else None
        raise RuntimeError("save failed") from e
