---
name: update
description: Refresh the course harness in this repo from the published template — skills, scripts, the schedule, and assignment files the instructor maintains. Shows what would change before writing anything and never touches the student's own work. Use when the student says /update, asks to get the latest skills or course files, or when something in the harness looks out of date or broken.
---

Bring this repo's harness up to date with what the instructor has published.

This repo was created from a template, so it shares no history with it and `git pull` cannot
deliver instructor fixes. `scripts/harness_update.py` does that instead: it reads a manifest of
the files the instructor maintains and downloads only the ones that differ.

## Step 1 — show the student what would change

Run the preview. It writes nothing:

```
python3 scripts/harness_update.py
```

Report what it prints, in plain terms. Translate the file list into what it means for them: a
changed `SKILL.md` means one of their commands behaves differently, a changed
`course-schedule.json` means a due date moved, a changed `weeks/weekNN/README.md` means an
assignment was corrected.

A `remove` line means the instructor retired that file and nothing in the course uses it any
more. Say which file and that it is going, so a deletion never arrives unannounced. The script
only ever removes a harness file, never one of theirs, and refuses every path in the protected
list below whatever the manifest asks for.

If it reports nothing pending, say so and stop. Do not run `--apply` when there is nothing to do.

If it fails on the network, say plainly that the update needs internet and nothing was changed.
Do not retry in a loop — the script already backs off and gives up on its own.

The same run also checks the course materials repo, the sibling folder with lecture decks and
quiz banks, and reports it under a "Course materials" heading. This is a separate git repository
that `harness_update.py` cannot pull as part of the harness, so it checks it directly. Tell the
student what it found: if the folder is missing, give them the clone command it prints; if it is
behind, name the decks and quiz banks that would arrive; if it is already current, say so. A
materials problem never changes whether the harness update itself succeeded.

## Step 2 — commit anything of theirs that is outstanding

Check `git status --short` before applying. If the student has uncommitted work, commit it first
(or let them decide to), so the harness update lands as its own commit and stays easy to undo.

The script refuses to overwrite any file with uncommitted changes and reports it as skipped, so
a student who has edited a harness file will not silently lose it. If that happens, tell them
which file, and that they can commit or discard their version to accept the published one.

## Step 3 — apply, then commit it on its own

```
python3 scripts/harness_update.py --apply
```

Then commit the refresh by itself, so `git revert` on one commit puts the harness back:

```
git add -A
git commit -m "Update course harness"
```

Push it. Tell the student what changed in behavior, not just which files moved.

If a skill file changed, mention that Claude Code loads skills at session start, so they should
start a fresh session before relying on the updated command.

This same `--apply` run also pulls the course materials repo, if it found one behind and on a
clean `main`. Tell the student what arrived there too. That repo is separate from this one and
is never part of the `git add -A` commit above; it has its own history and its own `git pull`.

## Where the decks and quiz banks live

After an update, the lecture deck for a given week is at:

```
<materials folder>/decks/SPAX-402-Week-NN-student.pdf
```

and that week's quiz bank is at:

```
<materials folder>/weeks/weekNN/quiz-bank.md
```

`<materials folder>` is the course materials repo, normally a sibling folder next to this one
named `spax402-course-materials`. If a student cannot find it, run
`python3 scripts/materials_path.py` to locate it, or follow the clone instructions this skill
prints when the folder is missing.

## What this never touches

The script protects these regardless of what the manifest says, and you must not work around it:

- `weeks/*/BRIEF.md` — their brief, always typed by them
- `weeks/*/checks/` — quiz and audit artifacts, which are graded
- `weeks/*/outputs/` and any `data/raw/` — their results and source data
- `learning-records/` and `lessons/` — what `/teach` has built up for them
- `my-skills/` — skills they author from Week 9 on; this is theirs, not the harness
- `MISSION.md` — their own words about what they want out of the course

If a student asks you to update one of those from the template, decline and explain that it is
their work. If they believe a protected file is genuinely broken, that is a question for the
instructor, not something to overwrite.

## Integrity

Never edit `harness-manifest.json` locally to force an outcome, never fetch a harness file by
hand to sidestep the script's checks, and never disable the protections above. If the script and
the student disagree about what should happen, the script wins and the instructor settles it.
