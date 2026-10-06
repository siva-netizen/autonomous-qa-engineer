"""Fail closed when committed source/config contains obvious secrets or injection markers."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".venv", "node_modules", "shopdemo", "artifacts", "__pycache__"}
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".ts", ".tsx", ".js", ".mjs"}
SECRET_PATTERNS = (
    re.compile(r"gsk_[A-Za-z0-9]{20,}"),
    re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?:GROQ|GEMINI|OPENAI|ANTHROPIC)_API_KEY\s*=\s*(?!\s*(?:#|$))[A-Za-z0-9_./:+-]{8,}"),
)
INJECTION_MARKERS = (
    "ignore previous instructions",
    "disregard all prior instructions",
    "reveal the system prompt",
)


def candidate_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


def main() -> int:
    findings: list[str] = []
    for path in candidate_files():
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                findings.append(f"secret-shaped value in {relative}")
        if any(marker in content.lower() for marker in INJECTION_MARKERS) and (
            ".kiro/agents" in str(relative) or str(relative).startswith("agents/")
        ):
            findings.append(f"prompt-injection marker in {relative}")

    if findings:
        print("Security scan failed:")
        print("\n".join(f"- {finding}" for finding in findings))
        return 1
    print(f"Security scan passed: {len(candidate_files())} text files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
