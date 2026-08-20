# Week 5 — Intro to Regression Modeling

## Objectives

By Monday night you can:
- fit and read a simple linear regression, and say in plain English what the slope means in the
  units of the problem;
- explain what a control variable does to a coefficient, and why "the coefficient moved" is the
  interesting event rather than a nuisance;
- recognize a confounded relationship in sports data and name the mechanism, rather than just
  asserting "correlation isn't causation";
- say why the unit of analysis you choose (game vs. season) decides whether you can answer the
  question at all.

## The question

**Does running the ball win games, or does winning make you run?**

Every coach has heard "establish the run." The data appears to agree, loudly. Your job this week
is to find out whether it actually does.

## Thursday (in class, pairs, by hand, no AI)

Two printed sheets. Nothing beyond a calculator or a small spreadsheet.

1. **Ten team-games.** Each row has rush attempts and final point margin. Compute the slope of
   margin on rush attempts by hand, from the formula. You will get a large positive number. Write
   down, in one sentence, the advice that number appears to give a coach.

2. **Forty plays**, each tagged with the score situation it was run in. Compute the share of plays
   that were runs, separately for each of the five situations. You will get five fractions. Look
   at the order they come in before you do anything else.

Keep both. Sheet 1 is the result you will have to explain away. Sheet 2 is the explanation.

If you need more time, finish at home Thursday evening, before you start the take-home. No need to
ask.

## The take-home (this repo, solo)

1. Pull four seasons of play-by-play (`data/pull_pbp.py`, same safety pattern as Week 1: read it
   with your agent first). Four seasons, not one, and you should be able to say why before you run
   it.

2. Build a **team-game** table: for each team in each game, its rush attempts, its total plays, and
   its final point margin. Have your agent reproduce your ten hand-computed rows from Thursday, and
   match them, before you trust the other two thousand.

3. **Fit the naive model:** margin ~ rush attempts. Export the full regression output to `outputs/`
   as .xlsx. Note the coefficient, the p-value, and the R².

4. **Add one control:** the average score differential the team faced across its own plays in that
   game. Fit margin ~ rush attempts + score state. Export this one too.

5. **Rebuild your Thursday mechanism table at full scale**, one row per score bucket, one column
   per season. Export it.

6. Produce one chart that makes the confound visible to somebody who will not read a regression
   table.

**Verify:** your five Thursday fractions should reappear, in the same order, in step 5. If they do
not, something is wrong with your filter, not with the NFL.

## Your brief (BRIEF.md — typed by you)

For a coach who is about to tell his offensive coordinator to run more:

- What does the naive model say the advice should be, and how confident does it look?
- What happens to that advice once you account for score state, and what is the mechanism? Explain
  it in terms a coach would recognize from his own game-planning, not in terms of coefficients.
- The controlled effect does not disappear. It shrinks by roughly 85% and stays statistically
  significant. Give the two competing explanations for what survives, and say what you would need
  in order to tell them apart.
- Would you run this on 32 team-seasons instead of 2,174 team-games? Say specifically what breaks.

## Before you push

`/audit`, then `/quiz-me`. The question bank lives in the materials repo, so `git pull`
there first. Submission = repo link in Canvas, Monday 11:59pm,
green check on your latest commit.
