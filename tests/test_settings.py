import json

import pytest
from fastapi.testclient import TestClient

from gym import reviewer
from gym.app import create_app
from tests.conftest import FIXTURES


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "g-test")
    monkeypatch.setenv("GROQ_API_KEY", "q-test")
    monkeypatch.setenv("GROQ_MODEL", "some/model")


def test_settings_list_providers_with_models_and_key_status(tmp_path, keys, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY")
    client = TestClient(create_app(FIXTURES, tmp_path / "p.db"))
    s = client.get("/api/settings").json()
    assert s["provider"] == "gemini"
    by_id = {p["id"]: p for p in s["providers"]}
    assert by_id["gemini"]["configured"] is True and by_id["groq"]["configured"] is False
    assert by_id["groq"]["model"] == "some/model"
    assert client.post("/api/settings", json={"provider": "groq"}).status_code == 400  # no key


def test_switching_provider_is_remembered_and_validated(tmp_path, keys):
    path = tmp_path / "p.db"
    client = TestClient(create_app(FIXTURES, path))
    assert client.post("/api/settings", json={"provider": "nope"}).status_code == 400
    assert client.post("/api/settings", json={"provider": "groq"}).json()["provider"] == "groq"
    assert TestClient(create_app(FIXTURES, path)).get("/api/settings").json()["provider"] == "groq"


def test_reviews_use_the_selected_provider(tmp_path, keys, monkeypatch):
    seen = []

    def fake(name):
        def call(prompt):
            seen.append(name)
            return json.dumps({"scores": [4, 4, 4, 4], "verdict": "v", "feedback": "f"})
        return call

    monkeypatch.setitem(reviewer.PROVIDERS, "gemini", ("Gemini", fake("gemini"), "GEMINI_API_KEY", "GEMINI_MODEL", "m"))
    monkeypatch.setitem(reviewer.PROVIDERS, "groq", ("Groq", fake("groq"), "GROQ_API_KEY", "GROQ_MODEL", "m"))
    client = TestClient(create_app(FIXTURES, tmp_path / "p.db"))
    body = {"exercise_id": "explain-count-words", "text": "answer"}
    assert client.post("/api/review", json=body).json()["status"] == "done"
    client.post("/api/settings", json={"provider": "groq"})
    assert client.post("/api/review", json=body).json()["status"] == "done"
    assert seen == ["gemini", "groq"]


def test_progress_reset_keeps_the_provider_choice(tmp_path, keys):
    client = TestClient(create_app(FIXTURES, tmp_path / "p.db"))
    client.post("/api/settings", json={"provider": "groq"})
    client.post("/api/progress/reset", json={})
    assert client.get("/api/settings").json()["provider"] == "groq"
