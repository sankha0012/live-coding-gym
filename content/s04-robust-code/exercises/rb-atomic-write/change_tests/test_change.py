import json
import os
import shutil
import tempfile

from solution import atomic_write_json


def _dir():
    return tempfile.mkdtemp(), shutil.rmtree


def _text(p):
    with open(p) as f:
        return f.read()


def test_indent_pretty_prints():
    d, rm = _dir()
    try:
        p = os.path.join(d, "s.json")
        obj = {"a": [1, 2], "b": {"c": None}}
        atomic_write_json(p, obj, indent=2)
        assert _text(p) == json.dumps(obj, indent=2)
        assert "\n" in _text(p)
        atomic_write_json(p, obj, indent=4)
        assert _text(p) == json.dumps(obj, indent=4)
        assert os.listdir(d) == ["s.json"]
    finally:
        rm(d)


def test_default_is_compact_single_line():
    d, rm = _dir()
    try:
        p = os.path.join(d, "s.json")
        atomic_write_json(p, {"a": [1, 2]}, indent=None)
        assert _text(p) == json.dumps({"a": [1, 2]})
        assert "\n" not in _text(p)
    finally:
        rm(d)


def test_failure_with_indent_keeps_old_file_and_no_temp():
    d, rm = _dir()
    try:
        p = os.path.join(d, "s.json")
        atomic_write_json(p, {"v": 1}, indent=2)
        before = _text(p)
        try:
            atomic_write_json(p, {"v": object()}, indent=2)
            raised = False
        except TypeError:
            raised = True
        assert raised
        assert _text(p) == before
        assert os.listdir(d) == ["s.json"]
    finally:
        rm(d)
