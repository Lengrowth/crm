#!/usr/bin/env python3
"""Fail on high-confidence secret material without printing matching content."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b"),
    re.compile(r"(?i)(?:api[_-]?key|api[_-]?secret)\s*[:=]\s*['\"][^'\"]{16,}['\"]"),
)
IGNORED_PARTS = {".git", "node_modules", ".next", "__pycache__", ".venv"}


def tracked_and_untracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    )
    paths = [Path(raw) for raw in result.stdout.decode().split("\0") if raw]
    return [path for path in paths if not any(part in IGNORED_PARTS for part in path.parts)]


def main() -> int:
    findings: list[str] = []
    for path in tracked_and_untracked_files():
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(pattern.search(content) for pattern in PATTERNS):
            findings.append(path.as_posix())

    if findings:
        print("Potential secret material found in files:", file=sys.stderr)
        for path in findings:
            print(f"- {path}", file=sys.stderr)
        print("Matching content is intentionally omitted.", file=sys.stderr)
        return 1

    print("Secret scan passed: no high-confidence credential patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
