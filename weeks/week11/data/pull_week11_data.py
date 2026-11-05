#!/usr/bin/env python3
"""Pull the Week 11 season snapshots: games played and games remaining, five leagues.

You do not need to run this. The CSV files next to it are the snapshot the assignment uses,
taken on Wednesday, November 4, 2026. It is here so you can see exactly where the data came
from, and so you can re-pull a later snapshot if you want to see how your predictions are
doing.

    python3 weeks/week11/data/pull_week11_data.py              # rewrite all five sports
    python3 weeks/week11/data/pull_week11_data.py nhl epl      # just these
    python3 weeks/week11/data/pull_week11_data.py --cutoff 2026-12-01

A game counts as played when the source marks it final and it was played before the cutoff
date (US Eastern). Everything else in the regular season is remaining, with blank scores.

Sources (all public, no key needed):
    nfl  nflverse games.csv (github.com/nflverse/nfldata)
    nba  ESPN public scoreboard API, one request per game date
    nhl  NHL public API (api-web.nhle.com), one club schedule per team
    cfb  ESPN public scoreboard API, FBS (groups=80), one request per week
    epl  fixturedownload.com
Standings for the check at the end come from ESPN, and from the NHL API for hockey.
"""
import argparse
import csv
import io
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import requests

try:
    from zoneinfo import ZoneInfo
    EASTERN = ZoneInfo("America/New_York")
except Exception:  # no tz database installed; a fixed offset is close enough for dates
    from datetime import timedelta
    EASTERN = timezone(timedelta(hours=-5))

HERE = Path(__file__).resolve().parent
CUTOFF = date(2026, 11, 4)
UA = "SPAX402-course-data-pull/1.0 (University of Delaware class assignment)"
PAUSE = 0.4          # seconds between requests, to be polite
MAX_TRIES = 5        # then fail loudly
ESPN = "https://site.api.espn.com/apis/site/v2/sports"
ESPN_STANDINGS = "https://site.api.espn.com/apis/v2/sports"

session = requests.Session()
session.headers["User-Agent"] = UA


def get(url, params=None, as_json=True):
    """GET with a retry limit and exponential backoff. Raises after MAX_TRIES."""
    wait = 2.0
    for attempt in range(1, MAX_TRIES + 1):
        try:
            r = session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                time.sleep(PAUSE)
                return r.json() if as_json else r.text
            if r.status_code not in (429, 500, 502, 503, 504):
                raise RuntimeError("%s returned HTTP %s" % (url, r.status_code))
            problem = "HTTP %s" % r.status_code
        except (requests.ConnectionError, requests.Timeout) as e:
            problem = type(e).__name__
        if attempt == MAX_TRIES:
            raise RuntimeError("%s failed %d times (last: %s)" % (url, MAX_TRIES, problem))
        print("  %s on %s, retrying in %.0fs" % (problem, url, wait), file=sys.stderr)
        time.sleep(wait)
        wait *= 2


def us_date(iso_utc):
    """An ISO UTC timestamp as the US Eastern calendar date."""
    t = datetime.fromisoformat(iso_utc.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t.astimezone(EASTERN).date()


def write(sport, rows, extra):
    """Split rows into played and remaining and write both with identical columns."""
    cols = ["date", "home", "away", "home_score", "away_score"] + extra
    rows = sorted(rows, key=lambda r: (r["date"], r["home"]))
    played = [r for r in rows if r["final"] and r["date"] < CUTOFF.isoformat()]
    remaining = [r for r in rows if not (r["final"] and r["date"] < CUTOFF.isoformat())]
    for r in remaining:
        r["home_score"] = r["away_score"] = ""
        if "ot" in r:
            r["ot"] = ""
    for name, part in (("played", played), ("remaining", remaining)):
        with open(HERE / ("%s_%s.csv" % (sport, name)), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore",
                               lineterminator="\n")
            w.writeheader()
            w.writerows(part)
    print("%s: %d played, %d remaining" % (sport, len(played), len(remaining)))
    return played, remaining


# ---------------------------------------------------------------- NFL

NFL_DIV = {
    "AFC East": "BUF MIA NE NYJ", "AFC North": "BAL CIN CLE PIT",
    "AFC South": "HOU IND JAX TEN", "AFC West": "DEN KC LAC LV",
    "NFC East": "DAL NYG PHI WAS", "NFC North": "CHI DET GB MIN",
    "NFC South": "ATL CAR NO TB", "NFC West": "ARI LA SEA SF",
}
NFL_TEAM_DIV = {t: d for d, ts in NFL_DIV.items() for t in ts.split()}


def pull_nfl():
    text = get("https://github.com/nflverse/nfldata/raw/master/data/games.csv", as_json=False)
    rows = []
    for g in csv.DictReader(io.StringIO(text)):
        if g["season"] != "2026" or g["game_type"] != "REG":
            continue
        h, a = g["home_team"], g["away_team"]
        final = g["home_score"] != "" and g["away_score"] != ""
        rows.append({
            "date": g["gameday"], "week": g["week"], "home": h, "away": a,
            "home_score": g["home_score"], "away_score": g["away_score"],
            "neutral": int(g["location"] == "Neutral"),
            "home_conf": NFL_TEAM_DIV[h][:3], "away_conf": NFL_TEAM_DIV[a][:3],
            "home_div": NFL_TEAM_DIV[h], "away_div": NFL_TEAM_DIV[a], "final": final,
        })
    return write("nfl", rows, ["week", "neutral", "home_conf", "away_conf", "home_div",
                               "away_div"])


# ---------------------------------------------------------------- ESPN helpers

def espn_standings(path, params=None):
    """{team displayName: (group name, {stat name: value})} from an ESPN standings feed."""
    data = get("%s/%s/standings" % (ESPN_STANDINGS, path), params)
    out = {}

    def walk(node, group):
        name = node.get("name") or group
        for e in node.get("standings", {}).get("entries", []):
            stats = {}
            for s in e.get("stats", []):
                key = s.get("name") or s.get("type")
                if key not in stats:
                    stats[key] = s.get("value", s.get("displayValue"))
                if s.get("type"):
                    stats.setdefault(s["type"], s.get("value", s.get("displayValue")))
            out[e["team"]["displayName"]] = (name, stats)
        for child in node.get("children", []):
            walk(child, name)

    walk(data, data.get("name"))
    return out


def espn_game(ev):
    c = ev["competitions"][0]
    side = {t["homeAway"]: t for t in c["competitors"]}
    st = c["status"]["type"]
    return c, side, st


# ---------------------------------------------------------------- NBA

def pull_nba():
    first = get("%s/basketball/nba/scoreboard" % ESPN, {"dates": "20261020"})
    days = sorted({d[:10] for d in first["leagues"][0]["calendar"]})
    conf = {t: g for t, (g, _) in espn_standings("basketball/nba").items()}
    rows, seen = [], set()
    for d in days:
        data = get("%s/basketball/nba/scoreboard" % ESPN, {"dates": d.replace("-", "")})
        for ev in data.get("events", []):
            if ev["season"]["type"] != 2 or ev["id"] in seen:
                continue
            seen.add(ev["id"])
            c, side, st = espn_game(ev)
            if st["name"] == "STATUS_CANCELED":
                continue
            h, a = side["home"]["team"]["displayName"], side["away"]["team"]["displayName"]
            if h not in conf or a not in conf:  # all-star or exhibition teams
                continue
            rows.append({
                "date": us_date(ev["date"]).isoformat(), "home": h, "away": a,
                "home_score": side["home"].get("score", ""),
                "away_score": side["away"].get("score", ""),
                "neutral": int(bool(c.get("neutralSite"))),
                "home_conf": conf[h].replace(" Conference", ""),
                "away_conf": conf[a].replace(" Conference", ""),
                "final": bool(st["completed"]),
            })
    return write("nba", rows, ["neutral", "home_conf", "away_conf"])


# ---------------------------------------------------------------- NHL

def pull_nhl():
    standings = get("https://api-web.nhle.com/v1/standings/now")["standings"]
    info = {s["teamAbbrev"]["default"]: s for s in standings}
    rows, seen = [], set()
    for abbrev in sorted(info):
        sched = get("https://api-web.nhle.com/v1/club-schedule-season/%s/20262027" % abbrev)
        for g in sched["games"]:
            if g["gameType"] != 2 or g["id"] in seen:
                continue
            seen.add(g["id"])
            h, a = g["homeTeam"]["abbrev"], g["awayTeam"]["abbrev"]
            final = g["gameState"] in ("OFF", "FINAL")
            last = g.get("gameOutcome", {}).get("lastPeriodType", "")
            name = lambda ab: info[ab]["teamName"]["default"]
            rows.append({
                "date": g["gameDate"], "home": name(h), "away": name(a),
                "home_score": g["homeTeam"].get("score", "") if final else "",
                "away_score": g["awayTeam"].get("score", "") if final else "",
                "ot": int(last in ("OT", "SO")) if final else "",
                "neutral": int(bool(g.get("neutralSite"))),
                "home_conf": info[h]["conferenceName"], "away_conf": info[a]["conferenceName"],
                "home_div": info[h]["divisionName"], "away_div": info[a]["divisionName"],
                "final": final,
            })
    return write("nhl", rows, ["ot", "neutral", "home_conf", "away_conf", "home_div",
                               "away_div"])


# ---------------------------------------------------------------- College football

def pull_cfb():
    fbs = {t: g for t, (g, _) in espn_standings("football/college-football",
                                                 {"group": "80"}).items()}
    rows, seen, skipped = [], set(), []
    for week in range(1, 16):
        data = get("%s/football/college-football/scoreboard" % ESPN,
                   {"groups": "80", "seasontype": "2", "week": str(week), "year": "2026",
                    "limit": "500"})
        for ev in data.get("events", []):
            if ev["id"] in seen:
                continue
            seen.add(ev["id"])
            c, side, st = espn_game(ev)
            notes = " ".join(n.get("headline", "") for n in c.get("notes", []))
            h, a = side["home"]["team"]["displayName"], side["away"]["team"]["displayName"]
            if "Championship" in notes:  # conference title games are what you simulate
                skipped.append(("title game", h, a, notes))
                continue
            if st["name"] == "STATUS_CANCELED":
                skipped.append(("canceled", h, a, notes))
                continue
            fcs = int(h not in fbs or a not in fbs)
            final = bool(st["completed"])
            if fcs and not final:
                skipped.append(("FCS opponent, not yet played", h, a, notes))
                continue  # remaining games are FBS against FBS only
            rows.append({
                "date": us_date(ev["date"]).isoformat(), "week": week, "home": h, "away": a,
                "home_score": side["home"].get("score", ""),
                "away_score": side["away"].get("score", ""),
                "neutral": int(bool(c.get("neutralSite"))),
                "home_conf": fbs.get(h, "FCS"), "away_conf": fbs.get(a, "FCS"),
                "conf_game": int(bool(c.get("conferenceCompetition"))),
                "fcs_opponent": fcs, "final": final,
            })
    for why, h, a, notes in skipped:
        print("  cfb left out (%s): %s vs %s %s" % (why, h, a, notes))
    return write("cfb", rows, ["week", "neutral", "home_conf", "away_conf", "conf_game",
                               "fcs_opponent"])


# ---------------------------------------------------------------- Premier League

def pull_epl():
    rows = []
    for m in get("https://fixturedownload.com/feed/json/epl-2026"):
        final = m["HomeTeamScore"] is not None and m["AwayTeamScore"] is not None
        rows.append({
            "date": m["DateUtc"][:10], "home": m["HomeTeam"], "away": m["AwayTeam"],
            "home_score": m["HomeTeamScore"] if final else "",
            "away_score": m["AwayTeamScore"] if final else "", "final": final,
        })
    return write("epl", rows, [])


PULLS = {"nfl": pull_nfl, "nba": pull_nba, "nhl": pull_nhl, "cfb": pull_cfb, "epl": pull_epl}


def main():
    global CUTOFF
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sports", nargs="*", default=list(PULLS), choices=list(PULLS))
    ap.add_argument("--cutoff", default=CUTOFF.isoformat(),
                    help="first date that counts as remaining (YYYY-MM-DD)")
    args = ap.parse_args()
    CUTOFF = date.fromisoformat(args.cutoff)
    for s in args.sports:
        PULLS[s]()


if __name__ == "__main__":
    main()
