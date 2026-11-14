from pathlib import Path

import pytest

from gym.content import load_content

FIXTURES = Path(__file__).parent / "fixtures" / "content"


@pytest.fixture
def steps():
    return load_content(FIXTURES)[0]


@pytest.fixture
def conn(tmp_path):
    from gym import db

    return db.connect(tmp_path / "data" / "progress.db")
