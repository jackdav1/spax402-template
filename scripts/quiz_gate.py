"""
The completeness report.

A week is checked when either of these is true:
  * its due date has passed (from course-schedule.json), or
  * its BRIEF.md has an answer under at least one question, meaning the student started
    submitting it early. A brief that only holds the instructor's questions does not count:
    scripts/new_brief.py creates it that way, so its mere existence proves nothing.

A checked week wants three things: a written brief, a quiz artifact whose `pass` is true, and a
transcript backing that artifact. Missing items are reported as warnings, never as a failure:
submitting an incomplete week is always allowed, and incompleteness is graded as part of the
case study's analysis half rather than blocked here.

This is a report, not a security boundary. It says what exists and what does not. Whether the
understanding behind the artifacts is real is what the closed-book quiz is for.

Instructor override: an `EXCUSED` file in a week's checks/ directory skips that week entirely.

Exit is 0 unless the repo or schedule itself is broken; warnings are printed for anything
missing so the student (and the instructor) can see the gaps.
"""

import json
import re
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "course-schedule.json"


COMMENT = re.compile(r"<!--.*?-->", re.S)


def brief_answered(path):
    """True when a BRIEF.md holds the student's own writing.

    new_brief.py seeds the file with the week's questions as headings and its instructions
    as an HTML comment, so "the file exists and is not empty" no longer distinguishes a
    written brief from an untouched one. Everything that is neither a heading nor a comment
    is the student's answer.
    """
    if not path.exists():
        return False
    body = COMMENT.sub("", path.read_text(encoding="utf-8"))
    return any(line.strip() and not line.lstrip().startswith("#")
               for line in body.splitlines())


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
    if not brief_answered(brief):
        if brief.exists():
            problems.append("%s: BRIEF.md still holds only the questions, and it was due "
                            "(%s). Answer them under the headings; your brief is typed by "
                            "you." % (week, reason))
        else:
            problems.append("%s: no BRIEF.md, and it was due (%s). Create it with "
                            "`python3 scripts/new_brief.py %s`, then answer the questions "
                            "in your own words." % (week, reason, week))
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
        started = brief_answered(brief)
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
            print("::warning::%s" % p)
        print("\nSubmission accepted with %d gap(s) above. Gaps count against the analysis "
              "half of the case study grade." % len(problems))
    elif not checked and not skipped:
        print("Nothing due yet and nothing started. Green, but you have not submitted anything.")
    else:
        print("\nAll %d checked week(s) are complete." % len(checked))


if __name__ == "__main__":
    main()
