#!/usr/bin/env python3
"""Refresh the course harness in this repo from the published course template.

Your repo was created from a template, which means it shares no history with it and
`git pull` cannot bring you instructor fixes. This script closes that gap: it reads a
manifest of the files the instructor maintains, compares them to what you have, and
downloads only what changed.

It touches the harness and nothing else. Your analyses, briefs, quiz artifacts, learning
records, and anything under `my-skills/` are unreachable from here by design (see
`is_protected` below), and it refuses to overwrite a file you have uncommitted changes in.

    python3 scripts/harness_update.py            # report what would change, write nothing
    python3 scripts/harness_update.py --apply    # download and write the changes
    python3 scripts/harness_update.py --check    # one-line staleness summary, never fails

Exit codes: 0 when the report succeeded (whether or not updates are pending), 1 when the
network, the manifest, or the repo itself was the problem. `--check` always exits 0.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_REPO = "jackdav1/spax402-template"
DEFAULT_REF = "main"
MANIFEST_NAME = "harness-manifest.json"

REPO_ENV = "SPAX402_TEMPLATE_REPO"
REF_ENV = "SPAX402_TEMPLATE_REF"
MANIFEST_ENV = "SPAX402_MANIFEST_URL"
# Points the whole fetch somewhere else, including a file:// URL. Used to test this script
# against a local checkout before anything is published.
BASE_ENV = "SPAX402_TEMPLATE_RAW_BASE"

TIMEOUT = 20
MAX_ATTEMPTS = 3
BACKOFF_BASE = 1.5

# Nothing under these may ever be written or deleted, no matter what a manifest claims.
# A bad manifest is a possibility; losing a student's semester is not.
PROTECTED_PREFIXES = (
    "my-skills/",
    "learning-records/",
    "lessons/",
    ".git/",
    ".claude/settings",
)
PROTECTED_PARTS = ("/checks/", "/outputs/", "/data/raw/")
PROTECTED_NAMES = ("BRIEF.md", "MISSION.md")

# Files the harness delivers once and then never touches again. The hand-build worksheets
# ship blank, the student fills them in and commits them in place, and from that moment the
# file on disk is their work under a harness-managed name. Protecting them outright would
# mean never delivering them at all, and the alternative is worse than it sounds: once the
# filled-in sheet is committed it is no longer uncommitted, so the ordinary update path sees
# a managed file whose hash does not match and restores the blank one over an evening's work.
DELIVER_ONCE_SUFFIXES = ("-worksheet.xlsx",)


def is_deliver_once(relpath):
    """True for a managed file that may be added but must never be overwritten."""
    return relpath.replace("\\", "/").endswith(DELIVER_ONCE_SUFFIXES)


def is_protected(relpath):
    """True when a path belongs to the student rather than the harness."""
    posix = relpath.replace("\\", "/")
    if posix.startswith(PROTECTED_PREFIXES):
        return True
    if any(part in "/" + posix for part in PROTECTED_PARTS):
        return True
    return posix.rsplit("/", 1)[-1] in PROTECTED_NAMES


def git_blob(relpath):
    """The content git has staged for a path, or None when it tracks no such file.

    Hashing the working copy directly would be wrong on Windows: git stores LF and checks
    out CRLF, so every text file would look permanently out of date. Git's own blob is
    byte-for-byte what raw.githubusercontent.com serves, so both sides agree.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "blob", ":%s" % relpath],
            capture_output=True, check=False,
        )
    except OSError:
        return read_normalized(ROOT / relpath)
    if result.returncode != 0:
        return None
    return result.stdout


def read_normalized(path):
    """Fallback for a repo without git: read bytes, and normalize newlines if it's text."""
    if not path.is_file():
        return None
    body = path.read_bytes()
    if b"\x00" in body:
        return body
    return body.replace(b"\r\n", b"\n")


def sha256_bytes(body):
    return hashlib.sha256(body).hexdigest()


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def raw_base():
    override = os.environ.get(BASE_ENV)
    if override:
        return override if override.endswith("/") else override + "/"
    repo = os.environ.get(REPO_ENV, DEFAULT_REPO)
    ref = os.environ.get(REF_ENV, DEFAULT_REF)
    return "https://raw.githubusercontent.com/%s/%s/" % (repo, ref)


def manifest_url():
    return os.environ.get(MANIFEST_ENV) or (raw_base() + MANIFEST_NAME)


def fetch(url):
    """Download one URL, with a capped number of attempts and exponential backoff.

    Raises the last error rather than returning something half-formed.
    """
    last = None
    for attempt in range(MAX_ATTEMPTS):
        if attempt:
            time.sleep(BACKOFF_BASE ** attempt)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "spax402-harness-update"})
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return response.read()
        except urllib.error.HTTPError as err:
            # A 404 will not become a 200 on retry; only back off on transient statuses.
            if err.code in (403, 429) or err.code >= 500:
                last = err
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as err:
            last = err
            continue
    raise last


def load_manifest(quiet=False):
    """Fetch and validate the manifest. With quiet=True, return None instead of complaining.

    /submit calls this in quiet mode: a version check must never put noise, or a failure,
    between a student and a deadline.
    """
    url = manifest_url()
    try:
        raw = fetch(url)
    except Exception as err:
        if quiet:
            return None
        fail(
            "Could not download the harness manifest.\n"
            "\n"
            "    %s\n"
            "    %s\n"
            "\n"
            "This needs a working internet connection. Nothing has been changed; try again\n"
            "later, and tell your instructor if it keeps failing." % (url, err)
        )
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as err:
        if quiet:
            return None
        fail("The harness manifest at %s is not valid JSON (%s). Tell your instructor; do not\n"
             "try to work around this." % (url, err))
    if not isinstance(data.get("files"), dict) or not data["files"]:
        if quiet:
            return None
        fail("The harness manifest at %s lists no files. Tell your instructor." % url)
    return data


def tracked_files():
    """Every path git tracks here, so scratch files are never deletion candidates."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return {line.strip() for line in out.splitlines() if line.strip()}


def uncommitted_files():
    """Managed paths with uncommitted edits, which we refuse to overwrite."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def plan(manifest):
    """Work out what would change. Returns (adds, updates, deletes, blocked, unchanged)."""
    files = manifest["files"]
    prefixes = tuple(manifest.get("managed_prefixes", ()))
    dirty = uncommitted_files()
    tracked = tracked_files()

    adds, updates, deletes, blocked, unchanged = [], [], [], [], []

    for relpath in sorted(files):
        if is_protected(relpath):
            # The manifest should never list one of these. Say so loudly and skip it.
            blocked.append((relpath, "protected: this is your work, not the harness"))
            continue
        local = git_blob(relpath)
        if local is None:
            adds.append(relpath)
        elif sha256_bytes(local) == files[relpath].get("sha256"):
            unchanged.append(relpath)
        elif is_deliver_once(relpath):
            # Already here and different from the published copy, which for a worksheet
            # means it has been worked in. Leave it alone and do not report it as pending,
            # or every /update for the rest of the semester offers to erase it.
            unchanged.append(relpath)
        elif relpath in dirty:
            blocked.append((relpath, "you have uncommitted changes here"))
        else:
            updates.append(relpath)

    if tracked is not None:
        # Two ways a file gets removed. Inside a managed directory, absence from the manifest
        # is enough. Anywhere else the manifest has to name it, because we cannot tell a
        # retired harness file from a file the student made.
        retired = tuple(manifest.get("retired", ()))
        candidates = {relpath for relpath in tracked
                      if prefixes and relpath.startswith(prefixes)}
        candidates.update(relpath for relpath in retired if relpath in tracked)
        for relpath in sorted(candidates):
            if relpath in files:
                continue
            if is_protected(relpath):
                continue
            if relpath in dirty:
                blocked.append((relpath, "retired upstream, but you have uncommitted changes"))
            else:
                deletes.append(relpath)

    return adds, updates, deletes, blocked, unchanged


def download_into(relpath, expected_sha):
    """Fetch one managed file and write it, verifying the hash the manifest promised."""
    url = raw_base() + relpath
    body = fetch(url)
    got = hashlib.sha256(body).hexdigest()
    if expected_sha and got != expected_sha:
        raise ValueError(
            "%s downloaded but its checksum does not match the manifest.\n"
            "The template probably changed mid-run. Re-run this and it should settle." % relpath
        )
    target = ROOT / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)


def describe(adds, updates, deletes, blocked, unchanged, manifest):
    print("Harness manifest: %s" % manifest_url())
    if manifest.get("generated"):
        print("Published:        %s" % manifest["generated"])
    print("Up to date:       %d file(s)" % len(unchanged))
    print("")

    if not (adds or updates or deletes):
        print("Your harness matches the published version. Nothing to do.")
    else:
        for relpath in updates:
            print("  update   %s" % relpath)
        for relpath in adds:
            print("  add      %s" % relpath)
        for relpath in deletes:
            print("  remove   %s  (retired by your instructor)" % relpath)

    if blocked:
        print("")
        print("Skipped, on purpose:")
        for relpath, why in blocked:
            print("  %s  (%s)" % (relpath, why))
        print("")
        if any("protected" in why for _relpath, why in blocked):
            print("Protected files are yours and are never updated from the template. If one of")
            print("them looks wrong, ask your instructor rather than replacing it.")
        if any("uncommitted" in why for _relpath, why in blocked):
            print("For the files you have edited: commit or discard your version if you want the")
            print("published one instead. Nothing was touched either way.")


def apply_changes(adds, updates, deletes, files):
    written, removed = [], []
    for relpath in updates + adds:
        download_into(relpath, files.get(relpath, {}).get("sha256"))
        written.append(relpath)
    for relpath in deletes:
        target = ROOT / relpath
        if target.exists():
            target.unlink()
        removed.append(relpath)
    return written, removed


def check_mode(manifest):
    """One line for /submit. Never fails, never writes, silent when nothing is pending."""
    adds, updates, deletes, _blocked, _unchanged = plan(manifest)
    pending = len(adds) + len(updates) + len(deletes)
    if pending:
        print("Your course harness is %d file(s) behind the published version. "
              "Run /update when convenient." % pending)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                       help="write the changes instead of only reporting them")
    parser.add_argument("--check", action="store_true",
                       help="print a one-line staleness summary and always exit 0")
    args = parser.parse_args()

    if not (ROOT / "course-schedule.json").exists():
        if args.check:
            sys.exit(0)
        fail("This does not look like a SPAX 402 course repo (no course-schedule.json at %s)."
             % ROOT)

    if args.check:
        # A version check must never be what stands between a student and a deadline:
        # no network, no manifest, or a broken one all mean "say nothing, exit clean".
        manifest = load_manifest(quiet=True)
        if manifest is None:
            sys.exit(0)
        check_mode(manifest)

    manifest = load_manifest()
    adds, updates, deletes, blocked, unchanged = plan(manifest)
    describe(adds, updates, deletes, blocked, unchanged, manifest)

    if not args.apply:
        if adds or updates or deletes:
            print("")
            print("This was a preview. Re-run with --apply to make these changes.")
        return

    if not (adds or updates or deletes):
        return

    print("")
    try:
        written, removed = apply_changes(adds, updates, deletes, manifest["files"])
    except Exception as err:
        fail("Stopped partway through: %s\n"
             "\n"
             "Some files may already be updated. Re-run this to finish, or `git checkout .`\n"
             "to put the harness back the way it was." % err)

    for relpath in written:
        print("  wrote    %s" % relpath)
    for relpath in removed:
        print("  removed  %s" % relpath)
    print("")
    print("Done. %d written, %d removed. Commit this on its own so it is easy to undo:"
          % (len(written), len(removed)))
    print("")
    print("    git add -A && git commit -m \"Update course harness\"")


if __name__ == "__main__":
    main()
