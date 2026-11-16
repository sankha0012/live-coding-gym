"""Vercel entry point: the same FastAPI app, with progress kept in /tmp (it is lost when the function restarts)."""
import os

os.environ.setdefault("GYM_DB", "/tmp/gym.db")

from gym.app import create_app  # noqa: E402

app = create_app()
