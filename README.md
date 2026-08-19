# SPAX 402 — Your Course Repo

Predictive Analytics with Athletics Data · University of Delaware · Fall 2026

This repository is your working environment for the whole semester. You'll complete every case
study here, with Claude Code as your analytical agent. The course grades how well you **direct**
the agent, **verify** its work, and **communicate** what it means — not how fast you can get it
to spit out an answer.

## The two gears

- **Closed gear (no AI):** Thursday in class you build a small version of each week's method by
  hand, on paper or in a small spreadsheet. This is where you prove the understanding is yours.
  Tuesday quizzes and both exams are also closed-book, closed-AI.
  If you need more time on the Thursday hand-build, finish it at home that evening before you start
  the open gear. You do not need to ask, and you do not need a reason.
- **Open gear (this repo):** you direct Claude Code to scale the analysis up — real data, real
  size. Your hand-built version from Thursday is the reference answer you check the agent
  against.

**The agent computes; you conclude.** Your `BRIEF.md` each week is typed by you. Ask Claude to
critique your draft (`/coach-brief`) — never to write it.

## Your weekly workflow

1. **Thursday (in class):** hand-build the toy version. Then start the open gear: run `/teach`
   on the week's method, and spec the scale-up with your agent.
2. **Take-home:** complete the analysis. Check the agent's output against your toy version.
   Run `/audit` and respond to what it finds.
3. **Write `BRIEF.md`** in the week's folder — your words, half a page.
4. **Run `/quiz-me`** for the week. You can't submit without a passing quiz artifact.
5. **Commit and push everything**, then submit your repo link in Canvas by **Monday 11:59pm**.
   A green check on your latest commit means your submission is complete; a red X means it isn't.

## The skills

| Command | What it does |
|---|---|
| `/teach` | Teaches you the week's method Socratically. Learning records accumulate in this repo. |
| `/quiz-me` | The week's comprehension check. Mastery loop: wrong answers get taught, then re-asked. Everything is logged. |
| `/audit` | An adversarial reviewer goes hunting for flaws in your analysis: leakage, bad assumptions, wrong tails. |
| `/coach-brief` | Red-teams your hand-written brief draft like a skeptical coach. Critique only — it will not write for you. |

## Repo map

```
weeks/weekNN/         your work for each week
  README.md           the assignment: objectives, closed-gear recap, open-gear spec, brief questions
  quiz-bank.md        the week's core quiz questions (no answers — understanding is the answer key)
  data/raw/           source data — never edited, never deleted
  outputs/            exported results (.xlsx/.csv/charts) — always inspectable in Excel
  checks/             quiz + audit artifacts and transcripts (graded; do not edit by hand)
  BRIEF.md            your half-page brief to the coach — typed by you
learning-records/     what you've learned, accumulated by /teach across the semester
lessons/              reference lessons /teach builds for you
my-skills/            skills YOU author (Week 9+) — this is yours; the harness itself is not editable
```

## Honor code, in one line

Everything in `checks/` and every transcript is read by your instructor, the weekly verbal test
can land on you, and the closed-book layer always tells the truth about what you know.
