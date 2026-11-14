import json
import os
import shutil
import tempfile

from solution import atomic_write_json


def _dir():
    d = tempfile.mkdtemp()
    return d, shutil.rmtree


def test_creates_file():
    d, rm = _dir()
    try:
        p = os.path.join(d, "state.json")
        atomic_write_json(p, {"a": 1, "b": [1, 2]})
        with open(p) as f:
            assert json.load(f) == {"a": 1, "b": [1, 2]}
        assert os.listdir(d) == ["state.json"]
    finally:
        rm(d)


def test_overwrites_existing():
    d, rm = _dir()
    try:
        p = os.path.join(d, "state.json")
        atomic_write_json(p, {"v": 1})
        atomic_write_json(p, {"v": 2})
        with open(p) as f:
            assert json.load(f) == {"v": 2}
        assert os.listdir(d) == ["state.json"]
    finally:
        rm(d)


def test_failure_keeps_old_file_and_no_temp():
    d, rm = _dir()
    try:
        p = os.path.join(d, "state.json")
        atomic_write_json(p, {"v": 1})
        try:
            atomic_write_json(p, {"v": object()})
            raised = False
        except TypeError:
            raised = True
        assert raised
        with open(p) as f:
            assert json.load(f) == {"v": 1}
        assert os.listdir(d) == ["state.json"]
    finally:
        rm(d)


def test_failure_without_existing_file():
    d, rm = _dir()
    try:
        p = os.path.join(d, "new.json")
        try:
            atomic_write_json(p, {1, 2, 3})
            raised = False
        except TypeError:
            raised = True
        assert raised
        assert os.listdir(d) == []
    finally:
        rm(d)


def test_empty_object():
    d, rm = _dir()
    try:
        p = os.path.join(d, "e.json")
        atomic_write_json(p, {})
        with open(p) as f:
            assert json.load(f) == {}
    finally:
        rm(d)
