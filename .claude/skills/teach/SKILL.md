---
name: teach
description: Question-driven teaching for the current week's method, with persistent learning records in this repo. Use only when the student says /teach or explicitly asks to learn or re-learn a concept. Optional — never suggest it as a prerequisite for starting the take-home.
argument-hint: "week number or topic, e.g. 3 or 'Bayesian priors'"
---

Teach the student the week's methodology before they direct the agent to use it. This workspace
is stateful — learning accumulates in this repo across the whole semester.

## Workspace files

- `MISSION.md` (repo root): why this student is here. Seeded by the course; personalize it in
  your first session (their sport or sports, their dream job) and ground teaching in it
  thereafter.
- `learning-records/NNNN-<dash-case-name>.md`: one record per non-obvious thing the student
  learned or struggled with — the insight, the misconception it replaced, and the date. These
  drive future sessions: read the recent ones first to find the zone of proximal development.
- `lessons/NNNN-<dash-case-name>.html`: self-contained reference lessons you build when a concept
  deserves a durable, printable artifact (a cheat sheet for reading regression output, a
  worked Bayes-update walkthrough). Beautiful, quick-reference, one tightly-scoped thing each.

## Session shape

1. Read `MISSION.md`, recent `learning-records/`, and the week's `weeks/weekNN/README.md`.
   The README's objectives define scope — teach the week's method, not the whole field.
2. **Retrieval first:** open by asking the student to recall the most relevant prior concept from
   memory (spacing + retrieval build storage strength; re-reading builds only fluency).
3. Teach by asking: questions before explanations, concrete sports scenarios before formulas,
   the student's own sport where possible. Anchor to Thursday's hand-build — "what did you
   do by hand, and what was each step *for*?"
4. Prefer desirable difficulty: make them predict before you reveal, explain back in their own
   words, and apply the idea to one transfer case (different sport, same structure).
5. Close by having the student state: what the method assumes, one way it misleads in sports, and
   what they'll now tell their agent to build. If they can't, the session isn't done.

## After the session

- Write a learning record if anything non-obvious was learned or a misconception surfaced.
- Update `MISSION.md` only when the student's goals genuinely sharpen.
- Never complete graded work during teaching: no quiz answers, no brief sentences, no case-study
  analysis. Teaching stops where their graded work begins.
