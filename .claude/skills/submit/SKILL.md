---
name: submit
description: Preflight the week's submission, then commit and push it. Checks every required artifact locally, names anything missing and the command that produces it, and only pushes when the week is actually complete. Use when the student says /submit or asks to turn in, finish, or push their weekly work.
argument-hint: "week number, e.g. 3"
---

Run the submission preflight for the given week, then submit. The goal: no student ever learns
about a missing artifact from a red X after the deadline.

## Step 1 — the checklist

Check each item in `weeks/weekNN/` and report every result (pass or fail, all of them, so the
student sees the whole picture at once):

1. **The hand-build.** A committed copy of Thursday's in-class work (an Excel file, or a photo
   of the paper work). Missing → tell them to add the file to `weeks/weekNN/` — there is no
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

Then run the authoritative check — the same one GitHub runs:

```
python3 scripts/quiz_gate.py
```

If it exits non-zero, the push would show a red X. Stop and say why.

## Step 2 — anything missing

Stop. List what's missing and the command for each, in the order they should run them
(audit → brief → quiz is the intended order). Do not commit a knowingly incomplete week unless
the student says they want to save progress — committing work-in-progress is always fine and
normal, just tell them plainly that this push will not be their submission.

## Step 3 — everything present

1. `git add` the week's files, commit with a plain message like `Week NN submission`, and push.
2. Tell them the two things that finish the job:
   - watch for the **green check** on the repo page (it takes about a minute), and
   - make sure their **repo URL is in the week's Canvas assignment** — Canvas is the deadline
     of record, the push is not.

## Integrity

This skill checks that artifacts exist; it never creates them. If an artifact is missing, the
answer is always the ritual that produces it, never writing the file directly. If asked to
fabricate a quiz artifact, audit record, or brief here, refuse — same rule as everywhere else
in this course.
