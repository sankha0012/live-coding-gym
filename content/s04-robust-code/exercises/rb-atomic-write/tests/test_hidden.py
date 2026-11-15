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


def _spy_replace():
    calls = []
    real = os.replace

    def spy(src, dst, *a, **k):
        calls.append((os.path.abspath(src), os.path.abspath(dst)))
        return real(src, dst, *a, **k)

    os.replace = spy
    return calls, lambda: setattr(os, "replace", real)


def test_temp_in_same_directory_moved_with_os_replace():
    d, rm = _dir()
    calls, restore = _spy_replace()
    try:
        p = os.path.join(d, "state.json")
        atomic_write_json(p, {"v": 1})
        assert len(calls) == 1
        src, dst = calls[0]
        assert os.path.realpath(os.path.dirname(src)) == os.path.realpath(d)
        assert os.path.realpath(dst) == os.path.realpath(p) and src != dst
    finally:
        restore()
        rm(d)


def test_relative_path():
    d, rm = _dir()
    old = os.getcwd()
    calls, restore = _spy_replace()
    try:
        os.chdir(d)
        atomic_write_json("rel.json", {"v": 3})
        with open("rel.json") as f:
            assert json.load(f) == {"v": 3}
        assert os.listdir(d) == ["rel.json"]
        assert os.path.realpath(os.path.dirname(calls[0][0])) == os.path.realpath(d)
    finally:
        restore()
        os.chdir(old)
        rm(d)


def test_failure_in_replace_step_leaves_no_temp():
    d, rm = _dir()
    try:
        p = os.path.join(d, "taken")
        os.mkdir(p)  # os.replace of a file onto a directory fails
        try:
            atomic_write_json(p, {"v": 1})
            raised = False
        except OSError:
            raised = True
        assert raised
        assert os.listdir(d) == ["taken"] and os.path.isdir(p)
    finally:
        rm(d)


def test_original_exception_is_reraised():
    class Boom(Exception):
        pass

    class Bad(list):
        def __iter__(self):
            raise Boom("nope")

    d, rm = _dir()
    try:
        p = os.path.join(d, "state.json")
        atomic_write_json(p, {"v": 1})
        try:
            atomic_write_json(p, {"v": Bad([1])})
            assert False, "should raise"
        except Boom as e:
            assert str(e) == "nope"
        assert os.listdir(d) == ["state.json"]
        with open(p) as f:
            assert json.load(f) == {"v": 1}
    finally:
        rm(d)
