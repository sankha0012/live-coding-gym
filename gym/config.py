import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DB_PATH = ROOT / "data" / "progress.db"
WEB_DIR = ROOT / "web"


def load_env(path=ROOT / ".env"):
    """Read KEY=VALUE lines into os.environ without overriding existing values."""
    if not Path(path).exists():
        return
    for line in Path(path).read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
