#!/usr/bin/env python3
"""Regenerate harness-manifest.json. Instructor tool; students never need to run it.

The manifest is what `/update` reads to decide what a student's repo is missing. It is a
complete listing of the files the instructor maintains, so anything under a managed prefix
that is absent from the manifest is treated as retired and gets removed on update. That is
how a dropped skill disappears from every student repo instead of lingering. A file outside
those directories has to be named in RETIRED_FILES to be removed.

Run it in the template repo after changing any harness file, then commit the manifest in
the same commit as the change:

    python3 scripts/build_harness_manifest.py
    python3 scripts/build_harness_manifest.py --check   # CI-friendly, writes nothing

`--check` exits non-zero when the manifest on disk does not match the tree, which catches
a harness edit that was committed without regenerating the manifest.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "harness-manifest.json"

# Whole directories the instructor owns. Deletion propagates inside these: a tracked file
# here that is not in the manifest is removed on update.
MANAGED_PREFIXES = [
    ".claude/skills/",
    "scripts/",
    "setup/",
]

# Individual instructor-owned files. No deletion propagation, so these are safe to list
# even when they sit beside student work.
MANAGED_FILES = [
    ".github/workflows/harness-manifest.yml",
    ".github/workflows/quiz-gate.yml",
    ".gitignore",
    "CLAUDE.md",
    "README.md",
    "course-schedule.json",
    "weeks/week01/README.md",
    "weeks/week01/data/hand-build-nfl-entropy.csv",
    "weeks/week01/data/hand-build-nfl-entropy-worksheet.xlsx",
    "weeks/week01/data/pull_pbp.py",
    "weeks/week02/README.md",
    "weeks/week02/data/hand-build-nfl-field-goals.csv",
    "weeks/week02/data/hand-build-nfl-field-goals-worksheet.xlsx",
]

# Files this harness used to ship and no longer does. Deletion propagates only inside
# MANAGED_PREFIXES, so a retired file that sat anywhere else would linger in every student
# repo forever. Listing it here removes it on the next update.
#
# Only ever list a path the harness itself published. A student's own file is not ours to
# delete, and harness_update refuses the protected ones whatever this says. An entry can be
# dropped once every repo has updated past it; leaving it costs nothing.
RETIRED_FILES = [
    "BRIEF-template.md",
]

# Never manage these, even by accident. Kept in step with harness_update.is_protected.
NEVER = ("MISSION.md",)


def staged_blob(relpath):
    """Git's staged content for a path: LF-normalized, and exactly what raw GitHub serves.

    Hashing the working copy would break on Windows, where git checks text out as CRLF.
    Stage your harness edits before running this, or the manifest describes the old file.
    """
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", ":%s" % relpath],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def tracked():
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout
    return sorted(line.strip() for line in out.splitlines() if line.strip())


def collect():
    prefixes = tuple(MANAGED_PREFIXES)
    paths = set()

    for relpath in tracked():
        if relpath.startswith(prefixes):
            paths.add(relpath)

    for relpath in MANAGED_FILES:
        if not (ROOT / relpath).is_file():
            print("warning: %s is listed as managed but does not exist; skipping." % relpath,
                  file=sys.stderr)
            continue
        paths.add(relpath)

    for name in NEVER:
        paths.discard(name)

    files = {}
    for relpath in sorted(paths):
        body = staged_blob(relpath)
        if body is None:
            print("warning: %s is not staged in git; skipping it. Run `git add` first."
                  % relpath, file=sys.stderr)
            continue
        files[relpath] = {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
    return files


def retired(files):
    """The retired list, checked against the manifest we just built.

    A path that is both managed and retired is a contradiction: the update would write the
    file and then delete it. Fail rather than publish that.
    """
    both = sorted(set(RETIRED_FILES) & set(files))
    if both:
        sys.exit("%s listed as both managed and retired. Pick one." % ", ".join(both))
    for relpath in RETIRED_FILES:
        if (ROOT / relpath).is_file():
            print("warning: %s is listed as retired but still exists here. Delete it in the "
                  "template, or take it off the retired list." % relpath, file=sys.stderr)
    return sorted(RETIRED_FILES)


def build():
    files = collect()
    return {
        "generated": date.today().isoformat(),
        "source": "jackdav1/spax402-template@main",
        "managed_prefixes": MANAGED_PREFIXES,
        "retired": retired(files),
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                       help="verify the manifest matches the tree; write nothing")
    args = parser.parse_args()

    fresh = build()

    if args.check:
        if not MANIFEST.is_file():
            print("::error::%s does not exist. Run this script without --check."
                  % MANIFEST.name)
            sys.exit(1)
        on_disk = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if on_disk.get("files") != fresh["files"] or \
                on_disk.get("managed_prefixes") != fresh["managed_prefixes"] or                 on_disk.get("retired", []) != fresh["retired"]:
            print("::error::%s is stale. A harness file changed without regenerating it.\n"
                  "Run: python3 scripts/build_harness_manifest.py" % MANIFEST.name)
            sys.exit(1)
        print("%s is current (%d files)." % (MANIFEST.name, len(fresh["files"])))
        return

    MANIFEST.write_text(json.dumps(fresh, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote %s - %d managed file(s), %d retired"
          % (MANIFEST.name, len(fresh["files"]), len(fresh["retired"])))


if __name__ == "__main__":
    main()
