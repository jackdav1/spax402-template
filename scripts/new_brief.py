#!/usr/bin/env python3
"""Create this week's BRIEF.md from the questions the instructor wrote.

The brief is the week's questions and your answers to them, nothing else. The questions
live in course-schedule.json, which the harness update ships, so a week's brief always
matches the assignment the instructor published.

    python3 scripts/new_brief.py week01

It writes weeks/week01/BRIEF.md with each question as a heading and blank space under it.
It never touches a brief that already exists: your answers are yours, and a script that
could overwrite them would be worse than no script.

Exit codes: 0 when the file was written, 1 when it was not (already there, unknown week,
bad schedule file).
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "course-schedule.json"

HEADER = """# Brief — %(week_label)s: %(title)s

<!-- Written for %(audience)s. Every word below is yours: the agent may critique this
     draft (/coach-brief), never write it. Half a page total. Answer each question in a
     few sentences, in language your audience would use. Write under the headings; the
     quiz gate reads anything outside a heading or a comment as your answer. -->
"""


def load_brief(week):
    if not SCHEDULE.is_file():
        sys.exit("%s is missing. Run /update to restore the harness." % SCHEDULE.name)
    try:
        data = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        sys.exit("%s is not valid JSON (%s). Run /update to restore it."
                 % (SCHEDULE.name, err))

    briefs = data.get("brief") or {}
    if week not in briefs:
        known = ", ".join(sorted(briefs)) or "none yet"
        sys.exit("No brief questions for %s in %s. Weeks available: %s. If this week's "
                 "assignment is out, run /update to get its questions."
                 % (week, SCHEDULE.name, known))
    return briefs[week]


def questions_of(brief):
    """Every question in the week, in order, whether or not the week has parts.

    A week with two case studies lists them under `parts`, each with its own title and
    audience. Anything that only wants the questions reads them through here, so a week
    with parts and a week without behave the same.
    """
    if brief.get("parts"):
        return [q for part in brief["parts"] for q in part["questions"]]
    return list(brief["questions"])


def render(week, brief):
    week_label = "Week %s" % week.replace("week", "").lstrip("0")
    out = [HEADER % {
        "week_label": week_label,
        "title": brief.get("title", ""),
        "audience": brief.get("audience", "the audience named in the week's README"),
    }]
    # Numbering runs straight through the week rather than restarting inside each part, so a
    # question can be named by its number alone in class and in the audit.
    n = 0
    for part in brief.get("parts") or [brief]:
        if brief.get("parts"):
            out.append("\n# %s\n\n<!-- Written for %s. -->\n"
                       % (part.get("title", ""), part.get("audience", "")))
        for question in part["questions"]:
            n += 1
            out.append("\n## %d. %s\n\n\n" % (n, question))
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("week", help="the week folder, e.g. week01")
    args = ap.parse_args()

    week = args.week.strip().strip("/").replace("weeks/", "")
    weekdir = ROOT / "weeks" / week
    if not weekdir.is_dir():
        sys.exit("%s does not exist. Check the week name." % weekdir.relative_to(ROOT))

    target = weekdir / "BRIEF.md"
    if target.exists():
        sys.exit("%s already exists, so nothing was written. Open it and keep writing."
                 % target.relative_to(ROOT).as_posix())

    brief = load_brief(week)
    target.write_text(render(week, brief), encoding="utf-8")
    print("wrote %s with %d questions to answer."
          % (target.relative_to(ROOT).as_posix(), len(questions_of(brief))))


if __name__ == "__main__":
    main()
