# Week 2 — Probability, the Binomial, and Confidence Intervals

## Objectives

By Tuesday night you can:
- state the probability of an event, its complement, and a probability conditioned on a
  situation, and say in words what each one means;
- use the binomial distribution to get the chance of a given number of successes in a fixed
  number of attempts, in Excel and by hand;
- build a 95% confidence interval on a rate from the count of successes and the number of
  attempts, and explain what the interval does and does not claim;
- decide whether two rates are far enough apart to be treated as different, and say what
  sample size you would need before that question has an answer;
- adjust a rate for the difficulty of the attempts behind it, and explain why the adjustment
  changes the ranking.

## Thursday (in class, by hand, no agentic AI)

Open `data/hand-build-nfl-field-goals-worksheet.xlsx` and fill in every highlighted cell. It
holds all 27 field goal attempts by Dustin Hopkins in the 2024 regular season and playoffs,
one row per kick, with the distance and the result. You compute his make rate, its standard
error, the 95% margin of error, both ends of the interval, and whether that interval contains
the league's make rate. The same rows are in `data/hand-build-nfl-field-goals.csv` if you
would rather build the sheet from scratch.

Use cell references rather than typing numbers back in. A sheet built on references still
gives the right answer when a row changes, and you will change rows in the Case Study.

Commit the filled-in worksheet where it already sits, in `weeks/week02/data/`. The hand-build
is part of the Tuesday, September 8 submission, and it is the number your agent has to
reproduce before you trust anything it computes for the whole league.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: which kickers can you actually tell apart?** A general manager wants to know
whether his kicker is a problem. Every kicker in the league has a make rate, they are all
different from each other, and almost none of those differences survive a confidence
interval. Your job is to find out which ones do. Direct your agent to:

1. Pull the season's play-by-play. The pull script from Week 1 is in
   `weeks/week01/data/pull_pbp.py` and the file it already downloaded is the one to use;
   there is no reason to download it twice. Field goal attempts are the plays where
   `play_type` is `field_goal`, and `field_goal_result` tells you what happened.
2. Compute, for every kicker with at least 20 attempts, the make rate, the standard error, and
   the 95% confidence interval. Count a blocked kick as a miss, or do not, but say which you
   chose and why. It changes the answer.
3. Compare each interval against the league's overall make rate, and count how many kickers
   you can separate from average in either direction.
4. Work out the make rate the whole league managed at each distance, then use it to get what an
   average kicker would have made from the attempts each kicker actually faced. Rank the
   kickers by how far above or below that they finished, and compare that ranking to the raw
   one.
5. **Verify:** the agent must reproduce your hand-computed kicker from Thursday, to the same
   standard error, before you accept any league-wide table. If the two disagree, the agent is
   wrong until proven otherwise.
6. Commit the code you ran, plus the tables or charts that back up your brief. `outputs/` is
   the place for them.

A note on question 4 in your brief. Solving for the sample size is algebra on the margin of
error formula, not a new method: fix the margin of error you want and solve for the number of
attempts. Do it in Excel and show the number.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week02
```

That writes `weeks/week02/BRIEF.md` with this week's questions as headings and space under
each. Your audience is a general manager, so he needs to know what to do about his kicker, not
what a standard error is. Answer every question in a few sentences, in your own words.
`/coach-brief 2` will critique a draft; it will not write one.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Tuesday, September 8 at
11:59pm. Labor Day moves this week's deadline off Monday. You can submit with items
missing; anything missing at the deadline counts against the analysis half of the grade.
