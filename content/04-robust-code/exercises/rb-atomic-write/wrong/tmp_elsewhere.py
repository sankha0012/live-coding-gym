import json
import os
import tempfile


def atomic_write_json(path: str, obj) -> None:
    fd, tmp = tempfile.mkstemp(suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
