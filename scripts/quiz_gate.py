"""
The quiz gate.

A week is checked when either of these is true:
  * its due date has passed (from course-schedule.json), or
  * it has a non-empty BRIEF.md, meaning the student started submitting it early.

A checked week needs three things: a written brief, a quiz artifact whose `pass` is true, and a
transcript backing that artifact. Any one missing is a red X.

This is a workflow gate, not a security boundary. It proves the artifacts exist and are internally
consistent. Whether the understanding behind them is real is what the closed-book quiz and the
verbal test are for.

Instructor override: an `EXCUSED` file in a week's checks/ directory skips that week entirely.

Exit 0 = green, exit 1 = red.
"""

import json
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "course-schedule.json"


def load_schedule():
    if not SCHEDULE.exists():
        print("::warning::%s is missing; only weeks with a BRIEF.md will be checked."
              % SCHEDULE.name)
        return {}, ZoneInfo("America/New_York")
    try:
        raw = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        print("::error::%s is not valid JSON (%s). Fix it: the gate cannot tell what is due."
              % (SCHEDULE.name, err))
        sys.exit(1)
    return raw.get("due", {}), ZoneInfo(raw.get("timezone", "America/New_York"))


def deadline_passed(date_str, tz, now):
    """Due at 11:59pm local time on the given date."""
    try:
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("::error::Bad date %r in %s; expected YYYY-MM-DD." % (date_str, SCHEDULE.name))
        sys.exit(1)
    return now > datetime.combine(day, time(23, 59), tzinfo=tz)


def check_week(week, weekdir, reason):
    """Return a list of problems for one week. Empty list means the week passes."""
    problems = []

    brief = weekdir / "BRIEF.md"
    if not brief.exists() or not brief.read_text(encoding="utf-8").strip():
        problems.append("%s: no BRIEF.md, and it was due (%s). Your brief is typed by you."
                        % (week, reason))
        # Without a brief the rest is moot, but keep checking so one push shows everything.

    artifact = weekdir / "checks" / ("%s-quiz.json" % week)
    if not artifact.exists():
        problems.append("%s: missing quiz artifact (%s). Run /quiz-me for this week."
                        % (week, artifact.relative_to(ROOT).as_posix()))
    else:
        try:
            data = json.loads(artifact.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            problems.append("%s: quiz artifact is not valid JSON (%s). Do not hand-edit files in "
                            "checks/; re-run /quiz-me." % (week, err))
            data = None
        if data is not None and data.get("pass") is not True:
            problems.append("%s: quiz artifact exists but `pass` is not true. Finish /quiz-me; the "
                            "mastery loop re-asks what you miss until you have it." % week)

    transcript = weekdir / "checks" / ("%s-quiz-transcript.md" % week)
    if not transcript.exists() or not transcript.read_text(encoding="utf-8").strip():
        problems.append("%s: quiz result is not backed by a transcript (%s)."
                        % (week, transcript.relative_to(ROOT).as_posix()))

    return problems


def main():
    due, tz = load_schedule()
    now = datetime.now(tz)

    weekdirs = sorted(p for p in (ROOT / "weeks").glob("week*") if p.is_dir())
    if not weekdirs:
        print("::error::No weeks/week* directories found. Is this the course repo?")
        sys.exit(1)

    problems, checked, skipped = [], [], []

    for weekdir in weekdirs:
        week = weekdir.name

        if (weekdir / "checks" / "EXCUSED").exists():
            skipped.append("%s (excused by instructor)" % week)
            continue

        brief = weekdir / "BRIEF.md"
        started = brief.exists() and bool(brief.read_text(encoding="utf-8").strip())
        overdue = week in due and deadline_passed(due[week], tz, now)

        if overdue:
            reason = "due %s" % due[week]
        elif started:
            reason = "submitted early"
        else:
            continue

        found = check_week(week, weekdir, reason)
        if found:
            problems.extend(found)
        else:
            checked.append("%s (%s)" % (week, reason))

    for line in skipped:
        print("skipped: %s" % line)
    for line in checked:
        print("OK: %s" % line)

    if problems:
        print("")
        for p in problems:
            print("::error::%s" % p)
        print("\nSubmission incomplete. %d problem(s) above." % len(problems))
        sys.exit(1)

    if not checked and not skipped:
        print("Nothing due yet and nothing started. Green, but you have not submitted anything.")
    else:
        print("\nAll %d checked week(s) pass the quiz gate." % len(checked))


if __name__ == "__main__":
    main()
