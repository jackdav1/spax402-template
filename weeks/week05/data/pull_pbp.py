"""
Pull four seasons of NFL play-by-play from nflverse.

Same shape as the Week 1 script, with one difference worth understanding before you run it: four
seasons instead of one. Ask yourself why a question about play-calling and winning needs more than
a single season, and be ready to answer it. You will be checking whether your finding is a fact
about football or a fact about 2024.

Read this with your agent before you run it.

Run it:  python pull_pbp.py
"""

import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

SEASONS = [2021, 2022, 2023, 2024]

URL = ("https://github.com/nflverse/nflverse-data/releases/download/pbp/"
       "play_by_play_{season}.parquet")

RAW = Path(__file__).parent / "raw"

# Same retry policy as Week 1: capped attempts, exponential backoff, a timeout on every request.
# Nothing here may loop forever, and nothing here may fail quietly.
MAX_ATTEMPTS = 4
BACKOFF_BASE_SECONDS = 2
TIMEOUT_SECONDS = 60

MIN_EXPECTED_ROWS = 40_000
EXPECTED_TEAMS = 32


def download_season(season):
    """Fetch one season, or confirm we already have it. Bounded retries, then a loud failure."""
    dest = RAW / "play_by_play_{}.parquet".format(season)
    if dest.exists():
        print("  {}: already have it ({:.1f} MB)".format(season, dest.stat().st_size / 1048576))
        return dest

    RAW.mkdir(parents=True, exist_ok=True)
    url = URL.format(season=season)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            # Download to a temporary name and rename only once every byte has arrived, so a
            # dropped connection can never leave a half-file wearing the real filename.
            partial = dest.with_suffix(".parquet.partial")
            with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
                partial.write_bytes(response.read())
            partial.replace(dest)
            print("  {}: downloaded {:.1f} MB".format(season, dest.stat().st_size / 1048576))
            return dest

        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as err:
            print("  {}: attempt {}/{} failed ({}: {})".format(
                season, attempt, MAX_ATTEMPTS, type(err).__name__, err))

            if attempt == MAX_ATTEMPTS:
                print("\nGiving up on {} after {} attempts. Nothing partial was kept.\n"
                      "Check your connection, then confirm this still resolves:\n  {}".format(
                          season, MAX_ATTEMPTS, url), file=sys.stderr)
                sys.exit(1)

            wait = BACKOFF_BASE_SECONDS ** attempt
            print("  {}: waiting {}s before retrying...".format(season, wait))
            time.sleep(wait)


def verify(path, season):
    """Confirm the file looks like a real NFL season before anybody trusts it."""
    df = pd.read_parquet(path, columns=["season", "season_type", "posteam", "play_type"])

    problems = []
    if len(df) < MIN_EXPECTED_ROWS:
        problems.append("only {:,} rows; expected at least {:,}".format(len(df), MIN_EXPECTED_ROWS))
    teams = df.posteam.dropna().nunique()
    if teams != EXPECTED_TEAMS:
        problems.append("{} distinct teams; expected {}".format(teams, EXPECTED_TEAMS))
    seasons = sorted(df.season.dropna().unique().tolist())
    if seasons != [season]:
        problems.append("season column contains {}; expected only [{}]".format(seasons, season))

    if problems:
        print("\n{} does not look right:".format(path.name), file=sys.stderr)
        for p in problems:
            print("  - {}".format(p), file=sys.stderr)
        print("\nDelete it and run again. If it fails the same way twice, stop and ask rather than "
              "analyzing data you have reason to distrust.", file=sys.stderr)
        sys.exit(1)

    return len(df)


def main():
    print("Pulling {} seasons: {}".format(len(SEASONS), SEASONS))
    total = 0
    for season in SEASONS:
        path = download_season(season)
        total += verify(path, season)

    print("\nAll {} seasons verified. {:,} plays total, in {}".format(len(SEASONS), total, RAW))
    print("\nNote what this script did NOT do. It did not build a team-game table, it did not")
    print("decide what counts as a rush, and it did not compute a single margin. Those are")
    print("choices, and this week is about the fact that choices like those decide answers.")


if __name__ == "__main__":
    main()
