# Week 1 — Review of Basic Statistics (+ getting this harness running)

## Objectives

By Monday night you can:
- describe a distribution's shape (skew, modality) and explain what it implies about the athletes
  or plays underneath it;
- compare variation across stats on different scales using the coefficient of variation;
- explain standardized entropy as a measure of unpredictability in play-calling, including what
  0 and 1 mean;
- run the full course workflow once, end to end: /teach → spec → verify → /audit → BRIEF.md →
  /quiz-me → push.

## Thursday (in class, by hand, no AI)

You built, by hand / small Excel:
1. Mean, SD, and coefficient of variation for a small set of NBA players' FG%, and a sketch of
   the distribution's shape.
2. Standardized entropy for **one team's** run/pass mix on 3rd/4th-and-short, on paper, from the
   formula.

Commit them (the Excel file, or a photo of the paper work) into `weeks/week01/` — the
hand-build is part of the Monday 11:59pm submission, and it is your reference answer for
the take-home.

Need more time? Finish the hand-build at home Thursday evening, before you start the take-home. No
need to ask.

## The take-home (this repo, solo)

**Case study: Entropy in the NFL.** Direct your agent to:
1. Pull the season's play-by-play from nflverse (the pull script is provided in `data/` — read it
   with your agent and have it explained to you, including how it limits and caches requests).
2. Filter to 3rd/4th-and-short situations, compute each team's run/pass split, standardized
   entropy, and first-down conversion rate.
3. **Verify:** the agent must reproduce your hand-computed team from Thursday and match your
   number before you accept the league-wide table.
4. Export the team table to `outputs/` as .xlsx and produce one chart relating entropy to
   conversion rate.

**Case study: NBA FG% by position.** Same pattern: distribution shape, group comparison, CV —
scaled to the full league, checked against your Thursday toy.

## Your brief (BRIEF.md — typed by you)

**Audience:** a head coach.

Answer:
- Do you see a relationship between play-calling unpredictability and converting short-yardage
  downs? Which team is the interesting outlier, and what's your best explanation?
- What other information would you want before telling a team to change its run/pass mix?
- How else would you compare scoring efficiency across positions beyond raw FG%?

## Before you push

`/audit`, then `/quiz-me`. Week 1's question bank ships in this repo. Submission = repo link
in Canvas, Monday 11:59pm, green check on your latest commit.
