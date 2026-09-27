#!/usr/bin/env python3
"""Minimal local validator for this Skill repository.

Checks the required Agent Skills files and basic SKILL.md frontmatter rules.
This is intentionally dependency-free so users can run it on a fresh clone.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> int:
    if not SKILL.exists():
        fail("SKILL.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail("YAML frontmatter closing marker is missing")

    fm = text[4:end]
    name_match = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    desc_match = re.search(r"^description:\s*>", fm, re.MULTILINE)

    if not name_match:
        fail("name field missing")
    name = name_match.group(1).strip()
    if not 1 <= len(name) <= 64:
        fail("name must be 1-64 characters")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("name must use lowercase letters, numbers and single hyphens")
    if name != ROOT.name:
        fail("name must match the parent directory name")
    if not desc_match:
        fail("description field missing or not using multiline form")

    required = [
        "README.md",
        "LICENSE.md",
        "NOTICE.md",
        "CHANGELOG.md",
        "references/onboarding.md",
        "references/persona-system.md",
        "references/persona-test.md",
        "references/topic-engine.md",
        "references/script-frameworks.md",
        "references/scene-directing.md",
        "references/live-streaming.md",
        "references/data-review.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            fail(f"required project file missing: {rel}")

    print("OK: drone-content-coach basic structure and SKILL.md checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
