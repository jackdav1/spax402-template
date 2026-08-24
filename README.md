# SPAX 402 — Your Course Repo

Predictive Analytics with Athletics Data · University of Delaware · Fall 2026

This repository is your working environment for the whole semester. You'll complete every case
study here, with Claude Code as your analytical agent. The course grades how well you **direct**
the agent, **verify** its work, and **communicate** what it means — not how fast you can get it
to spit out an answer.

## Every unit has four parts

- **Tuesday's lecture, in class.** The unit's concepts.
- **Thursday, in class, by hand, no agentic AI.** You build a small version of each week's method by
  hand, on paper or in a small spreadsheet. This is where you prove the understanding is yours.
  Tuesday quizzes and both exams are also closed-book, closed-AI.
  You may still use an LLM to help troubleshoot formulas and understand the approach.
  If you need more time on the hand-build, finish it at home that evening before you start the
  take-home. Commit the hand-build (the Excel file, or a photo of the paper work) with your
  Monday submission.
- **The take-home case study, on your own, with Claude Code, in this repo.** You direct Claude Code to scale the analysis
  up — real data, real size. Your hand-built version from Thursday is the reference answer
  you check the agent against.
- **Tuesday's quiz, closed-book, in class.** A short quiz at the start of Tuesday's class to
  confirm that you understand the concepts.

**The agent computes; you conclude.** Your `BRIEF.md` each week is typed by you. Ask Claude to
critique your draft (`/coach-brief`) — never to write it.

## Your weekly workflow

1. **Thursday (in class):** do the hand-build. Then start the take-home: run `/teach`
   on the week's method, and spec the scale-up with your agent.
2. **Take-home:** complete the analysis. Check the agent's output against your hand-build.
   Run `/audit` and respond to what it finds.
3. **Write `BRIEF.md`** in the week's folder — your words, half a page.
4. **Run `/quiz-me`** for the week. You can't submit without a passing quiz artifact.
5. **Run `/submit`** — it checks that nothing is missing, then commits and pushes. Make sure
   your repo link is in the week's Canvas assignment by **Monday 11:59pm**.

A green check on your latest commit means every week that is due has all three of: a written
`BRIEF.md`, a passed `/quiz-me` artifact, and the transcript backing it. A red X tells you which of
those is missing, by week. You can run the same check yourself before pushing:

```
python scripts/quiz_gate.py
```

Due dates live in `course-schedule.json`. The gate confirms your artifacts exist and agree with each
other; it cannot confirm you understand anything, which is what the Tuesday quiz is for.

## The skills

| Command | What it does |
|---|---|
| `/teach` | Teaches you the week's method Socratically. Learning records accumulate in this repo. |
| `/quiz-me` | The week's comprehension check. Mastery loop: wrong answers get taught, then re-asked. Everything is logged. |
| `/audit` | An adversarial reviewer goes hunting for flaws in your analysis: leakage, bad assumptions, wrong tails. |
| `/coach-brief` | Red-teams your hand-written brief draft as the week's named audience (usually a skeptical coach). Critique only — it will not write for you. |
| `/submit` | The submission preflight: checks every required artifact, tells you what's missing, and pushes when the week is complete. |

## Repo map

```
weeks/weekNN/         your work for each week
  README.md           the assignment: objectives, Thursday recap, take-home spec, brief questions
  data/raw/           source data — never edited, never deleted
  outputs/            exported results (.xlsx/.csv/charts) — always inspectable in Excel
  checks/             quiz + audit artifacts and transcripts (graded; do not edit by hand)
  BRIEF.md            your half-page brief to the week's audience — typed by you
learning-records/     what you've learned, accumulated by /teach across the semester
lessons/              reference lessons /teach builds for you
scripts/              helpers the harness runs (do not edit)
my-skills/            skills YOU author (Week 9+) — this is yours; the harness itself is not editable
```

## The materials repo

Two repositories, pointing opposite directions.

| | this repo | `spax402-course-materials` |
|---|---|---|
| named | `spax402-<your-name>` | `spax402-course-materials` |
| you | commit and push | pull only, never commit |
| holds | your work | decks, shared data, quiz banks |

Clone the materials repo **next to** this one, not inside it:

```
spax402-course-materials/   <- you pull
spax402-<your-name>/        <- you commit
```

Then `git pull` there each week. `/quiz-me` reads the week's question bank from that repo, so if
you have not cloned it the quiz cannot start. It will tell you so rather than making questions up.

If you keep it somewhere else, set `SPAX402_MATERIALS` to that path and everything still works.

## Honor code

Everything in `checks/` and every transcript is read by your instructor, and the closed-book
layer always tells the truth about what you know.
