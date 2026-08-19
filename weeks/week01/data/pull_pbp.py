"""
Pull one season of NFL play-by-play from nflverse.

Read this file with your agent before you run it. You should be able to explain, in your own
words, three things: where the data comes from, why the script refuses to download twice, and
what it checks after the download to decide the file is trustworthy. You will be asked.

What this script does NOT do: it does not filter, group, or analyze anything. It only puts a
raw season on your disk and confirms it arrived intact. The analysis is your job to direct.

Run it:  python pull_pbp.py
"""

import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

# --- Configuration ---------------------------------------------------------------------------

SEASON = 2024

# nflverse publishes each season as a single Parquet file attached to a GitHub release.
# Parquet is a columnar format: it stores each column separately, so reading 8 columns out of
# 380 costs almost nothing. That is why we do not use CSV here.
URL = (
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/"
    f"play_by_play_{SEASON}.parquet"
)

# data/raw is sacred. Nothing in this course ever writes to it except this script, and this
# script only ever writes to it once. Cleaned or derived data goes somewhere else, under a
# new name, produced by a script you can re-run.
RAW = Path(__file__).parent / "raw"
DEST = RAW / f"play_by_play_{SEASON}.parquet"

# Retry policy. Three ideas, and all three matter:
#   1. A capped number of attempts, so this can never loop forever.
#   2. Exponential backoff (2s, 4s, 8s), so a struggling server gets more room each time
#      rather than being hammered at a fixed interval.
#   3. A timeout on every single request, so one hung connection cannot stall the script
#      indefinitely. A request with no timeout is a bug, not a simpler request.
MAX_ATTEMPTS = 4
BACKOFF_BASE_SECONDS = 2
TIMEOUT_SECONDS = 60

# Sanity thresholds. A full NFL season is roughly 49,000 plays across 32 teams. These are
# deliberately loose: they are meant to catch a truncated download or an empty file, not to
# assert a precise number we would then have to maintain every year.
MIN_EXPECTED_ROWS = 40_000
EXPECTED_TEAMS = 32


# --- Download --------------------------------------------------------------------------------

def download_once() -> None:
    """Download the season file, retrying a bounded number of times, then give up loudly."""

    # The cache check. If the file is already here, we are done. Re-downloading 20 MB every
    # time you run an analysis is rude to the people hosting the data for free, and it makes
    # your own work slower for no benefit.
    if DEST.exists():
        size_mb = DEST.stat().st_size / 1_048_576
        print(f"Already have {DEST.name} ({size_mb:.1f} MB). Skipping download.")
        return

    RAW.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"Downloading {SEASON} play-by-play (attempt {attempt}/{MAX_ATTEMPTS})...")

            # Download to a temporary name first, then rename. If the connection dies
            # halfway, the partial file is never mistaken for a complete one, because the
            # real filename only appears once the bytes are all here.
            partial = DEST.with_suffix(".parquet.partial")
            with urllib.request.urlopen(URL, timeout=TIMEOUT_SECONDS) as response:
                partial.write_bytes(response.read())
            partial.replace(DEST)

            size_mb = DEST.stat().st_size / 1_048_576
            print(f"  Done: {size_mb:.1f} MB")
            return

        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as err:
            print(f"  Attempt {attempt} failed: {type(err).__name__}: {err}")

            if attempt == MAX_ATTEMPTS:
                # Fail loudly. Never swallow this and continue with no data, and never fall
                # back to some other silent behavior: the next thing that happens should be
                # a human reading this message, not an analysis running on nothing.
                print(
                    f"\nGiving up after {MAX_ATTEMPTS} attempts. Nothing was written.\n"
                    f"Check your internet connection, then confirm the URL still resolves:\n"
                    f"  {URL}",
                    file=sys.stderr,
                )
                sys.exit(1)

            wait = BACKOFF_BASE_SECONDS ** attempt
            print(f"  Waiting {wait}s before retrying...")
            time.sleep(wait)


# --- Verify ----------------------------------------------------------------------------------

def verify() -> pd.DataFrame:
    """Open the file and check it looks like a real NFL season before anyone trusts it."""

    print("\nVerifying the download...")

    # Read only the handful of columns we need to sanity-check. The full file has ~380.
    df = pd.read_parquet(
        DEST,
        columns=["season", "season_type", "posteam", "down", "ydstogo", "play_type"],
    )

    rows = len(df)
    teams = df.posteam.dropna().nunique()
    seasons = sorted(df.season.dropna().unique().tolist())
    kinds = df.season_type.value_counts().to_dict()

    print(f"  Rows:         {rows:,}")
    print(f"  Season(s):    {seasons}")
    print(f"  Teams:        {teams}")
    print(f"  Season types: {kinds}")

    # Each check states what would have to be wrong for it to fire. A check you cannot
    # explain is decoration.
    problems = []
    if rows < MIN_EXPECTED_ROWS:
        problems.append(f"only {rows:,} rows; expected at least {MIN_EXPECTED_ROWS:,}. Truncated?")
    if teams != EXPECTED_TEAMS:
        problems.append(f"{teams} distinct teams; expected {EXPECTED_TEAMS}.")
    if seasons != [SEASON]:
        problems.append(f"season column contains {seasons}; expected only [{SEASON}].")

    if problems:
        print("\nThis file does not look right:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            f"\nDelete {DEST.name} and run this script again. If it fails the same way twice,"
            " stop and ask, rather than analyzing data you have reason to distrust.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("  All checks passed.")
    return df


def main() -> None:
    download_once()
    df = verify()

    # One orienting fact, so you start from a number rather than from a blank screen.
    # Note what this is NOT: it is not your case study. It does not compute a run/pass split,
    # it does not compute entropy, and it does not touch a single team. Deciding how to define
    # "short yardage", which plays count, and what to do about scrambles and penalties is the
    # analytical work, and it is yours.
    playable = df[df.play_type.isin(["run", "pass"])]
    print(
        f"\n{len(playable):,} of {len(df):,} rows are ordinary run or pass plays."
        f"\nThe rest are kickoffs, punts, field goals, timeouts, penalties, and end-of-quarter"
        f" markers.\n\nRaw file: {DEST}"
    )
    print("\nNext: open a conversation with your agent about how you want to define the")
    print("situation you're studying. Do not let it pick the definition for you.")


if __name__ == "__main__":
    main()
