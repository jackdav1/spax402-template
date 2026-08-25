# Week 1 — Review of Basic Statistics (+ getting this harness running)

## Objectives

By Monday night you can:
- describe a distribution's shape (skew, modality) and explain what it implies about the athletes
  or plays underneath it;
- compare variation across stats on different scales using the coefficient of variation;
- explain standardized entropy as a measure of unpredictability in play-calling, including what
  0 and 1 mean;
- run the full course workflow once, end to end: spec → verify → /audit → BRIEF.md →
  /quiz-me → push. (/teach is optional, whenever you want a concept walked through.)

## Thursday (in class, by hand, no agentic AI)

You built, by hand / small Excel:
- Standardized entropy for **one team's** run/pass mix on 3rd/4th-and-short, in Excel, from the
  formula. Open `data/hand-build-nfl-entropy-worksheet.xlsx` and fill in every highlighted cell.
  It holds every Philadelphia Eagles run or pass play on 3rd or 4th down with exactly 2 yards to
  go, from the 2024 regular season and playoffs: 23 plays. The same rows are in
  `data/hand-build-nfl-entropy.csv` if you would rather build the sheet yourself.

Commit it (the Excel file) into `weeks/week01/` — the
hand-build is part of the Monday 11:59pm submission, and it is your reference answer for
the Case Study.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case Study. No
need to ask.

## The Case Study (this repo, solo)

**Case study: Entropy in the NFL.** The question: do less predictable play-callers have more
success in short yardage situations? Deciding what counts as success is your call, and you have to
defend the choice in your brief. Direct your agent to:
1. Pull the season's play-by-play from nflverse (the pull script is provided in `data/` — read it
   with your agent and have it explained to you, including how it limits and caches requests).
2. Filter to 3rd/4th-and-short situations, compute each team's run/pass split and standardized
   entropy, and measure success the way you defined it.
3. **Verify:** the agent must reproduce your hand-computed team from Thursday and match your
   number before you accept the league-wide table.
4. Export the team table to `outputs/` as .xlsx and produce one chart relating entropy to your
   success measure.

## Your brief (BRIEF.md — typed by you)

**Audience:** a head coach.

Answer:

- How did you define success in short yardage, and why that measure?
- Do you see a trend between standardized entropy and your measure of success?
- What other information would you want to look at to determine how important entropy is for
  success?
- How would you go about assessing the optimal entropy for a given team?

## Before you push

`/audit`, then `/quiz-me`. Week 1's question bank ships in this repo. Submission = repo link
in Canvas, Monday 11:59pm. You can submit with items missing; anything missing at the deadline
counts against the analysis half of the grade.
