"""Load project `.env` into os.environ without overriding existing variables."""

from __future__ import annotations

import os
from pathlib import Path


def load_project_dotenv(start: Path | None = None) -> None:
    path = (start or Path.cwd()) / ".env"
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        if not key or key in os.environ:
            continue
        cleaned = value.strip().strip('"').strip("'")
        os.environ[key] = cleaned
