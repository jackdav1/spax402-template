---
name: submit
description: Preflight the week's submission, then commit and push it. Checks every required artifact locally, names anything missing and the command that produces it, and always submits when the student says to — missing items are reported, never blocking. Use when the student says /submit or asks to turn in, finish, or push their weekly work.
argument-hint: "week number, e.g. 3"
---

Run the submission preflight for the given week, then submit. The goal: no student ever learns
about a missing artifact after the deadline. The checklist informs; it never blocks. If the
student wants to submit an incomplete week, submit it — gaps count against the analysis half of
the case study grade, and that is the student's call to make, not this skill's.

## Step 1 — the checklist

Check each item in `weeks/weekNN/` and report every result (pass or fail, all of them, so the
student sees the whole picture at once):

1. **The hand-build.** A committed copy of Thursday's in-class work (the Excel file).
   Missing → tell them to add the file to `weeks/weekNN/` — there is no
   command for this one, it's their own artifact.
2. **The analysis.** The scripts and outputs of the take-home case study.
3. **The audit record.** `checks/weekNN-audit.md`, containing findings with dispositions (or an
   explicit "checked, holds" list). Missing → run `/audit NN`.
4. **The brief.** `BRIEF.md`, non-empty and not the untouched template. Missing → set them up
   to write it: copy `BRIEF-template.md` to `weeks/weekNN/BRIEF.md`, tell them who this week's
   audience is (the `**Audience:**` line in the week's README), and remind them `/coach-brief NN`
   will critique a draft. **Never write or suggest a single sentence of the brief itself** —
   same hard rule as /coach-brief.
5. **The quiz.** `checks/weekNN-quiz.json` with `"pass": true`, plus its transcript. Missing or
   `pass: false` → run `/quiz-me NN`.

Then run the completeness report — the same one GitHub runs:

```
python3 scripts/quiz_gate.py
```

It warns on gaps; it does not fail on them.

Then check whether the harness itself is out of date:

```
python3 scripts/harness_update.py --check
```

This prints one line if the instructor has published newer skills or course files, and prints
nothing when there is nothing pending. It always exits 0 and needs the internet, so treat silence
and failure the same way: mention it if it says something, ignore it otherwise, and never let it
delay a submission. If it does report a gap, tell them `/update` will handle it **after** they
submit — a deadline is never the moment to change the harness.

## Step 2 — anything missing

List what's missing and the command for each, in the order they should run them
(audit → brief → quiz is the intended order). Then say plainly: they can submit right now with
these gaps. A missing hand-build, audit record, or quiz transcript counts against the analysis
half of the case study grade; a missing or empty BRIEF.md counts against the brief half. Or fill
the gaps first if there is time. Ask which they want. If they say submit, submit. Never refuse
to push, and never present completeness as a requirement for submitting.

## Step 3 — submitting

1. `git add` the week's files, commit with a plain message like `Week NN submission` (or
   `Week NN submission, incomplete` when gaps remain), and push.
2. Tell them the one thing that finishes the job: their **repo URL goes in the week's Canvas
   assignment** — Canvas is the deadline of record, the push is not.

## Integrity

This skill checks that artifacts exist; it never creates them. If an artifact is missing, the
answer is always the ritual that produces it, never writing the file directly. If asked to
fabricate a quiz artifact, audit record, or brief here, refuse — same rule as everywhere else
in this course.
