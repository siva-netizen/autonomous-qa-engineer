"""Safe repository file reads and test artifact writes for agent tool execution."""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CONTEXT_FILES: tuple[str, ...] = (
    "docs/SHOPDEMO_INSPECTION.md",
    "README.md",
)


class FileToolError(ValueError):
    """Raised when a path escapes the repository or I/O fails."""


def resolve_repo_path(relative: str) -> Path:
    candidate = (_REPO_ROOT / relative).resolve()
    if not candidate.is_relative_to(_REPO_ROOT):
        raise FileToolError(f"path escapes repository: {relative}")
    return candidate


def read_repo_text(relative: str, *, max_bytes: int = 512_000) -> str:
    path = resolve_repo_path(relative)
    if not path.is_file():
        raise FileToolError(f"missing file: {relative}")
    data = path.read_bytes()
    if len(data) > max_bytes:
        raise FileToolError(f"file too large: {relative}")
    return data.decode("utf-8")


def read_context_files(paths: tuple[str, ...] = DEFAULT_CONTEXT_FILES) -> dict[str, str]:
    loaded: dict[str, str] = {}
    for relative in paths:
        try:
            loaded[relative] = read_repo_text(relative)
        except FileToolError:
            continue
    return loaded


def write_repo_text(relative: str, content: str) -> Path:
    path = resolve_repo_path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def default_generated_test_path(request_id: str) -> str:
    slug = request_id.lower().replace("_", "-")
    return f"tests/e2e/generated/{slug}.spec.ts"
