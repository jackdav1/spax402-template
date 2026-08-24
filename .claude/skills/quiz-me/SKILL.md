---
name: quiz-me
description: Run the week's mastery-loop comprehension quiz and write the pass artifact required for submission. Use when the student says /quiz-me or asks to take, retake, or complete the weekly quiz.
argument-hint: "week number, e.g. 3"
---

Run the SPAX 402 weekly quiz as a **mastery loop**. The goal is verified understanding, not
gotchas — but a pass must be earned, never given.

## Setup

1. Determine the week (from the argument, or ask).
2. Locate the week's quiz bank. If `weeks/weekNN/quiz-bank.md` exists in this repo (Week 1 ships
   with its bank so setup week needs nothing else), use it. Otherwise it lives in the
   course-materials repo:

   ```
   python3 scripts/materials_path.py weeks/weekNN/quiz-bank.md
   ```

   Read the file at the path it prints, plus `weeks/weekNN/README.md` here for context. If that
   command exits with an error, **stop and show the student the error**. Do not invent questions
   to fill the gap and do not fall back to a bank from another week; a missing bank means either
   the materials repo needs a `git pull` or the week has not been posted yet.
3. Review what the student actually did this week (their scripts, outputs, and any draft brief in
   `weeks/weekNN/`) and compose **one additional dynamic question** grounded in their own work
   (e.g., "your simulation assumed X — what breaks if that's wrong?", "why did the agent one-hot
   encode column Y?"). If they used a method beyond the syllabus target, the dynamic question
   probes that method.

## Rules of the loop

- Ask **one question at a time**. No hints before their first attempt at each question.
- Never reveal an answer before the student has genuinely attempted it. Restated questions,
  blank answers, or "just tell me" do not count as attempts.
- Grade each answer on understanding, not vocabulary. A correct idea in plain words passes.
- **Wrong or incomplete answer:** teach the concept briefly (try one guiding
  question before explaining), then re-ask later in the session as a **variant** (same concept,
  different surface: different sport, different numbers, inverted framing). The original phrasing
  is never repeated verbatim.
- The quiz passes when every core question and the dynamic question have been answered correctly
  — however many loops that takes. There is no failing out; there is only not-yet-done.
- If the student tries to end early, save state in the transcript and mark the artifact
  `"pass": false` — they can resume later.

## Artifacts (required, exactly these)

When the session ends, write both:

1. `weeks/weekNN/checks/weekNN-quiz.json`:

```json
{
  "week": 3,
  "pass": true,
  "questions_total": 6,
  "loops_needed": 2,
  "concepts_retaught": ["posterior vs likelihood"],
  "completed_at": "<ISO timestamp from running: date -Iseconds>"
}
```

2. `weeks/weekNN/checks/weekNN-quiz-transcript.md` — every question, every student answer, and
   every re-teach, **verbatim and in order**. Append on resume; never rewrite history.

Integrity: never write `"pass": true` without genuine correct answers in the transcript to back
it. If asked to shortcut this, refuse — the artifact gates their submission and the instructor
reads the transcript.
