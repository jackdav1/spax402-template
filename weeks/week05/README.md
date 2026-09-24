# Week 5 — Correlation, Statistical Relationships, and Basic Regression Modeling

## Objectives

By Monday night you can:
- fit a line to two columns of data, and say in your own words what the slope, intercept,
  and residual mean;
- read a regression output table and explain what standard error, the confidence interval,
  and the p value tell you;
- understand why coefficients can clear 0.05 and still not be worth acting on due to
  chance, lurking variables, and small effect sizes.

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

The same ten games, plus a second column: each team's turnover differential that game,
takeaways minus giveaways, from nflverse play-by-play. For each game you compute the
predicted margin from the rushing slope and intercept, the residual, and the residual
squared. The block below turns those into the numbers Excel prints beside a regression: the
sum of squared residuals, the residual standard error (checked against STEYX), the standard
error of the slope (residual standard error divided by the square root of DEVSQ of x), t, the
two-sided p-value with T.DIST.2T, and the 95% interval with T.INV.2T. One check reads the
slope's standard error straight out of LINEST, with INDEX(LINEST(y range, x range, TRUE,
TRUE), 2, 1), so you can see the two routes agree.

Then you do the same for turnover differential in one step each: its slope, its standard
error from LINEST, its p-value and its interval. The two slopes are in different units,
points per rush attempt and points per turnover, so they cannot be compared directly. Take
each predictor's standard deviation with STDEV.S and multiply it by its slope to get how far
one standard deviation of each moves the margin.

### Sheet 3, `two predictors`

All thirty MLB teams in 2024: on-base percentage, slugging percentage and runs per game, from
the MLB Stats API. Runs per game is y and the two percentages are the two x columns.

Start with how closely the two predictors move together, with CORREL. Then fit each one
alone: its slope with SLOPE and its R squared with RSQ. Then fit both at once, which LINEST
does in one call. The formulas are written out on the sheet: INDEX(LINEST(y range, both x
columns, TRUE, TRUE), 1, 2) is the coefficient on OBP, INDEX(..., 1, 1) is the coefficient on
SLG, row 2 holds the standard errors and INDEX(..., 3, 1) is R squared. Then t and p for each
predictor.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week05/data/`. All three
sheets are part of the Monday, September 28 submission.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: does running the ball win games, or does winning make you run?** You work for
the Buffalo Bills. Joe Brady has just taken over as head coach and is looking back at the
seasons before him. Teams that run the ball more win more, and everyone in the building has
seen the chart. Coach Brady wants to know whether that means his team should run more, and he
wants the answer from you, not from the chart. Direct your agent to:

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
4. Build an interactive scatter of the 2,174 team-games, final margin against rush attempts,
   where hovering a point shows the team, opponent, week, score and `mean_score_diff`, and a
   control lets you colour or filter the points by season. A single HTML file is enough;
   commit it and open it in a browser. Your agent can build this in one pass, so ask for it
   directly.
5. Commit the code you ran, plus the tables, charts, and visuals that back up your brief.
   `outputs/` is the place for them.

Ask any clarifying questions before you start.

## The second Case Study (this repo, solo)

**Buy or sell at the deadline?** You work for a baseball club. It is the All-Star break, your
GM has to decide whether to trade for help or trade your own players away, and the decision
turns on one number: how many of the remaining games you are going to win.

Two models are already on the table, and they are the bar to beat. Predicting wins in games
82 to 162 from first-half wins alone, or from first-half run differential alone, each explains
about a third of the variation. Run differential is slightly the better of the two. Either one
is allowed in your model.

Your job is to try to beat them. Direct your agent to:

1. Start from `data/mlb-team-games-2014-2024.csv`, one row per team per game across eleven
   seasons: season, team, game number, game id, date, opponent, home or away, runs for, runs
   against, and whether the team won. Both sides of every game are there, so the opponent
   column is a real name you can look up. 2014 is included only so that the 2015 rows have a
   previous season behind them.
2. `data/mlb-team-first-half-lines-2015-2024.csv` has each team's batting and pitching line for
   each of its first 81 games, sharing the same game id: at-bats, hits, doubles, triples, home
   runs, walks, strikeouts, hit by pitch, sacrifice flies, stolen bases and runs on the batting
   side, and batters faced, outs, hits, home runs, walks, strikeouts, earned runs and runs on
   the pitching side. First half only, because the second half is the answer.
3. Two more files, both public:
   - `data/mlb-preseason-win-totals-2014-2024.csv`: each team's preseason Vegas win total
     (the over/under line), with the source for each row.
   - `data/mlb-injured-list-moves-2015-2024.csv`: every injured list move from MLB's
     transaction feed, one row per move: date, team, player, whether the player was placed,
     activated or transferred, the list length, and MLB's description.
4. Reproduce the two baselines first, so you know what you are trying to beat.
5. Then build something. Nothing in either file is a finished predictor; anything you want has
   to be constructed. Some questions worth asking: was a team's first-half record lucky, is its
   remaining schedule about to get harder or easier, what did it do last season, and do the
   underlying rates disagree with the run differential. There is more than one answer that
   works, and there is no reason for two people to find the same one.
6. Judge it with **adjusted R squared**, not R squared. R squared goes up whenever you add a
   column, so it cannot tell you whether a predictor earned its place. Adjusted R squared is
   the fourth line of the Excel regression output and your agent can compute it too.
7. Check that everything in your model was knowable at the All-Star break. A predictor built
   from the rest of the season will look excellent and be worthless, because in July nobody
   has it yet.
8. Commit the code and the output tables. `outputs/` again.

You may not beat the baselines by much. That is a real result and worth reporting honestly;
a model that adds nothing is a finding, not a failure.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week05
```

That writes `weeks/week05/BRIEF.md` with both case studies' questions as headings and space
under each, six in all. The brief is your thinking in your own words. Your code, tables, and
visuals are committed alongside it, so do not restate numbers the outputs already show; say
what they mean. Answer every question in a few sentences. `/coach-brief 5` will critique a
draft; it will not write one.

Each half has its own audience, and they want different things. Coach Brady needs to know
whether to change the game plan and what would convince him either way, not what a coefficient
is. The GM needs to know whether to buy or sell, which means he cares how much you trust your
own number.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, September 28 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
