---
name: verbal-test-prep
description: INSTRUCTOR ONLY — generate Verbal Test questions from a student's weekly submission. Run by Jack in a checkout of the student's repo after the Monday deadline.
argument-hint: "week number, e.g. 5"
disable-model-invocation: true
---

You are preparing Jack (the instructor) for Tuesday's Verbal Test: ~5 minutes with one randomly
drawn student about **their own** Monday submission, conducted while the rest of the class takes
the written quiz. It replaces the written quiz for that student. Scored 1 / 2 / 3.

## Read

The week's full submission: `BRIEF.md`, scripts and outputs, `checks/weekNN-quiz.json` and both
transcripts (quiz + audit). Look specifically for:

- concepts the quiz transcript shows they struggled with (looped on) — probe whether it stuck;
- audit findings they dispositioned as **accept** or **disclose** — probe whether the reasoning
  was theirs;
- the strongest claim in the brief — probe whether they can defend it without the repo open;
- anything the agent did that they may have waved through (a transformation, an encoding, a
  filter) — probe whether they know why it happened.

## Produce

3-4 questions, ordered easiest → hardest, each with:

- **Q:** the question, phrased to be asked out loud, about *their* work (quote their brief or
  their numbers back at them).
- **Good answer sounds like:** 2-3 sentences of what a 3 would say.
- **Red flags:** what a bluffing answer sounds like for this question.

Then a one-line scoring reminder: **3** = explains their own choices and assumptions unprompted;
**2** = understands the method but is shaky on their own submission's specifics; **1** = cannot
explain work submitted under their name.

Keep the whole output under one page — Jack reads it Tuesday morning between other things.
