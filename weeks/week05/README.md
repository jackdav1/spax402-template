# Week 5 — Correlation, Statistical Relationships, and Basic Regression Modeling

## Objectives

By Monday night you can:
- fit a line to two columns of data and say in words what the slope, the intercept and a
  residual mean;
- read a regression output table, say the null hypothesis out loud, and explain what the
  standard error, the confidence interval and the p-value each tell you;
- say why a coefficient that clears 0.05 can still be the wrong number to act on: chance, a
  lurking variable, or an effect too small to matter.

## Thursday (in class, in Excel, no agentic AI)

Open `data/hand-build-regression-worksheet.xlsx`. It has three sheets. The given numbers sit
in the left-hand columns, your answers go in the yellow cells, and the gray Check cell beside
each answer turns green when the answer is right. The check allows for rounding, so a value
you rounded to three decimals still turns green. Any gray left in a Check column is work still
to do.

Use cell references rather than typing numbers back in. Compute a mean once and point every
row at that cell.

### Sheet 1, `slope by hand`

Ten team-games from Week 8 of the 2021 NFL regular season, one side of each game: the team,
its opponent, its rush attempts and its final margin, from nflverse play-by-play. Rush
attempts are x and margin is y.

The four columns to the right of the data build the slope the long way: each x minus the
mean of x, each y minus the mean of y, their product, and the x deviation squared. The block
below sums the product column and the squared column, divides one by the other for the slope,
and gets the intercept from the two means. Then you check both against SLOPE and INTERCEPT,
take the correlation with CORREL and R squared with RSQ, predict the margin for a team that
runs thirty times, and compute the residual for one named team: its actual margin minus what
the line predicted.

### Sheet 2, `standard error and p`

The same ten games. For each one you compute the predicted margin from the slope and
intercept, the residual, and the residual squared. The block below turns those into the
numbers Excel prints beside a regression: the sum of squared residuals, the residual standard
error (checked against STEYX), the standard error of the slope (residual standard error
divided by the square root of DEVSQ of x), t, the two-sided p-value with T.DIST.2T, and the
95% interval with T.INV.2T. The last check reads the slope's standard error straight out of
LINEST, with INDEX(LINEST(y range, x range, TRUE, TRUE), 2, 1), so you can see the two
routes agree.

The sheet ends with a judgment cell that has no check: would you tell a coach these ten
games show that rushing more moves the margin? One sentence, and say which number you leaned
on.

### Sheet 3, `two predictors`

All thirty MLB teams in 2024: on-base percentage, slugging percentage and runs per game, from
the MLB Stats API. Runs per game is y and the two percentages are the two x columns, so this
is one regression with two predictors. LINEST does it in one call. The formulas are written
out on the sheet: INDEX(LINEST(y range, both x columns, TRUE, TRUE), 1, 2) is the coefficient
on OBP, INDEX(..., 1, 1) is the coefficient on SLG, row 2 holds the standard errors and
INDEX(..., 3, 1) is R squared. Then t and p for each predictor, the standard deviation of each
predictor across the thirty teams with STDEV.S, and each coefficient multiplied by its
standard deviation.

The OBP coefficient is about twice the SLG coefficient. The last cell asks which of the two
matters more to a team's runs, and what the case is for each answer.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week05/data/`. All three
sheets are part of the Monday, September 28 submission.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: does running the ball win games, or does winning make you run?** You work for
the Buffalo Bills. Teams that run the ball more win more, and everyone in the building has
seen the chart. Coach McDermott wants to know whether that means a team should run more, and
he wants the answer from you, not from the chart. Direct your agent to:

1. Start from `data/team-games-2022-2025.csv`. It is one row per team per regular-season
   game, 2,174 rows across four seasons, built from the nflverse play-by-play releases:
   season, week, game id, team, opponent, home or away, offensive plays, rush attempts, pass
   plays, run share, points for and against, final margin, and `mean_score_diff`, the average
   score differential the offense was facing across its snaps that game. A positive
   `mean_score_diff` is a team that spent most of the game ahead. The same rows can be rebuilt
   from the public `play_by_play_2022` through `play_by_play_2025` parquet files on the
   nflverse GitHub releases page, keeping regular-season plays that were a run or a pass.
2. Plot final margin against rush attempts with the fitted line, then regress margin on rush
   attempts and read the coefficient, its standard error, its p-value and R squared.
3. Add `mean_score_diff` as a second predictor and fit again. Compare the two rushing
   coefficients and the two R squared values side by side.
4. Open `data/plays-by-score-state-2022-2025.csv`, one row per team-game per score state:
   plays and rush attempts while the offense was down 9 or more, down 1 to 8, tied, up 1 to 8,
   and up 9 or more. Compute run share in each state, for all four seasons together and for
   each season on its own.
5. Refit both regressions one season at a time and say whether what you found in step 3 holds
   every year.
6. Build an interactive scatter of the 2,174 team-games, final margin against rush attempts,
   where hovering a point shows the team, opponent, week, score and `mean_score_diff`, and a
   control lets you colour or filter the points by score state or by season. A single HTML
   file is enough; commit it and open it in a browser. Your agent can build this in one pass,
   so ask for it directly.
7. Commit the code you ran, plus the tables, charts, and visuals that back up your brief.
   `outputs/` is the place for them.

Ask any clarifying questions before you start.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week05
```

That writes `weeks/week05/BRIEF.md` with this week's questions as headings and space under
each. The brief is your thinking in your own words. Your code, tables, and visuals are
committed alongside it, so do not restate numbers the outputs already show; say what they
mean. Your audience is Coach McDermott, so he needs to know whether to change the game plan
and what would convince him either way, not what a coefficient is. Answer every question in
a few sentences. `/coach-brief 5` will critique a draft; it will not write one.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, September 28 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
