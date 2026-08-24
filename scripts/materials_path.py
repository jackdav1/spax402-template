#!/usr/bin/env python3
"""Locate the course-materials repository that sits alongside this one.

Lecture decks, shared data, and the weekly quiz banks live in a second
repository (`spax402-course-materials`) that you pull and never commit to. This script
finds it and prints its path, so tooling never has to guess.

    python3 scripts/materials_path.py                       -> the repo root
    python3 scripts/materials_path.py weeks/week01/quiz-bank.md

It exits non-zero with an explanation if the repository is missing, rather than
letting anything carry on with a path that does not exist.
"""

import os
import sys
from pathlib import Path

MARKER = ".spax402-materials"
ENV_VAR = "SPAX402_MATERIALS"

REPO_ROOT = Path(__file__).resolve().parent.parent


def candidates():
    """Every place the materials repo is plausibly checked out, best guess first."""
    override = os.environ.get(ENV_VAR)
    if override:
        yield Path(override).expanduser()

    parent = REPO_ROOT.parent
    yield parent / "spax402-course-materials"
    yield parent / "spax402-materials"

    # A clone under any other name, as long as it is a sibling.
    if parent.is_dir():
        for sibling in sorted(parent.iterdir()):
            name = sibling.name.lower()
            if sibling.is_dir() and "spax402" in name and "material" in name:
                yield sibling

    yield Path.home() / "repos" / "spax402-course-materials"
    yield Path.home() / "repos" / "spax402-materials"
    yield Path.home() / "spax402-materials"


def find_materials():
    seen = set()
    for candidate in candidates():
        resolved = candidate.expanduser()
        key = str(resolved).lower()
        if key in seen:
            continue
        seen.add(key)
        if (resolved / MARKER).is_file():
            return resolved.resolve()
    return None


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    subpath = sys.argv[1] if len(sys.argv) > 1 else None

    root = find_materials()
    if root is None:
        fail(
            "Could not find the course-materials repository.\n"
            "\n"
            "It should be cloned next to this one:\n"
            "\n"
            f"    {REPO_ROOT.parent}\spax402-course-materials\n"
            f"    {REPO_ROOT}\n"
            "\n"
            "Clone it, or set the "
            f"{ENV_VAR} environment variable to where it already lives."
        )

    if subpath is None:
        print(root)
        return

    target = root / subpath
    if not target.exists():
        fail(
            f"Found the materials repo at {root}\n"
            f"but it has no {subpath}.\n"
            "\n"
            "Run `git pull` there. If it is still missing afterwards, that file has\n"
            "not been posted yet. Ask your instructor rather than working around it."
        )

    print(target)


if __name__ == "__main__":
    main()
