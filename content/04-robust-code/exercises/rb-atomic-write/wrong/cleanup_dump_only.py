import json
import os
import tempfile


def atomic_write_json(path: str, obj) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f)
    except BaseException:
        os.unlink(tmp)
        raise
    os.replace(tmp, path)
