# Week 6 — Regression Modeling Continued: Curves, Interactions, and Dummy Variables

## Objectives

By Monday night you can:
- decide whether a straight line, a curve, a dummy variable or an interaction fits the
  question, and say in words what each coefficient means;
- use a residual as a measure of how much a player beat what the model expected, and put it
  on a scale a coach can read.

## Thursday (in class, in Excel, no agentic AI)

Open `data/hand-build-regression-modeling-worksheet.xlsx`. It has three sheets, and all three
ask the same question: what is one more minute worth, and to whom? The given numbers sit in
the left-hand columns, your answers go in the yellow cells, and the gray Check cell beside each
answer turns green when the answer is right. The check allows for rounding. Any gray left in a
Check column is work still to do.

Each sheet starts with one yellow column you fill down: type the formula in the first row, then
double-click the fill handle (the small square at the bottom right of the cell) to copy it to
the last row. Then the yellow cells to the right, each with a plain-English line and its
formula.

The functions this week: RSQ, LINEST, INDEX and IF. LINEST(y range, x columns, TRUE, TRUE)
fits several predictors at once, and INDEX(LINEST(...), row, column) reads one number out of
it. Row 1 holds the coefficients, row 3 column 1 is R squared, and the coefficients come out in
reverse column order: the last x column first, the intercept last.

### Sheet 1, `curve`

Every NHL forward with at least 40 games in 2024-25, 397 players: points per game and average
time on ice in minutes, from the NHL stats API. Minutes are x and points per game is y.

Fill the minutes-squared column, then compare the straight line's R squared with the curve's,
fitted with LINEST on minutes and minutes squared. The last two cells use the curve to say how
many points over an 82-game season the 13th minute adds, and how many the 19th adds.

### Sheet 2, `forwards and defensemen`

Every skater with at least 40 games in 2024-25, 600 players: 397 forwards and 203 defensemen,
from the NHL stats API. Fill two columns: a dummy that is 1 for a defenseman and 0 for a
forward, with IF, and minutes times that dummy.

Fit the dummy alone first (minutes and the dummy), then add minutes times the dummy. The last
cells give a forward's points per extra minute and a defenseman's.

### Sheet 3, `minutes and usage`

Every NBA player with at least 40 games in 2024-25, 352 players: points and minutes per game
and usage rate, the percent of his team's possessions he ended while on the floor, from
Basketball-Reference.

Fill minutes times usage, fit minutes and usage without it and then with it, and use the
interaction model to say what one more minute is worth to a player who uses 15% of his team's
possessions and to one who uses 30%.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week06/data/`. All three
sheets are part of the Monday, October 5 submission.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: when do hitters peak?** You work for the Philadelphia Phillies. Dave
Dombrowski, the President of Baseball Operations, is weighing a five-year offer to a
30-year-old free agent hitter, and wants to know what the next five years of that bat are
likely to look like. Direct your agent to:

1. Start from `data/mlb-hitter-seasons-2008-2025.csv`, one row per player per season in which
   he batted at least once, 15,259 rows across seventeen seasons (2020's sixty-game season is
   left out), from the MLB Stats API: season, player id, name, birth date, age, games, plate
   appearances, at-bats, hits, doubles, triples, home runs, walks, strikeouts, hit by pitch,
   sacrifice flies, on-base percentage, slugging and OPS. Age is the player's age on June 30 of
   that season, the convention Baseball-Reference uses.
2. Keep the qualified seasons, 300 or more plate appearances, for ages 21 to 38. Plot OPS
   against age, fit a straight line, then a curve (add age squared as a second predictor), and
   find the age where the curve peaks.
3. Follow the same hitters. Pair each qualified season with the same player's next season,
   when he was one year older and also qualified (2019 and 2021 are two years apart, so they
   are not a pair). Average the change in OPS at each age, fit that change against age, and
   find the age where the average change crosses zero.
4. Build an interactive chart of OPS by age: pick one or more hitters by name and see each
   one's seasons drawn against the curves from steps 2 and 3, with hover showing the season,
   plate appearances and OPS. A single HTML file is enough; commit it and open it in a
   browser. Your agent can build this in one pass, so ask for it directly.
5. Commit the code you ran, plus the tables, charts, and visuals that back up your brief.
   `outputs/` is the place for them.

Ask any clarifying questions before you start.

## The second Case Study (this repo, solo)

**What is the 40 worth on draft day?** You work for the Buffalo Bills. Brandon Beane, the
President of Football Operations and General Manager, wants to know how much his staff should
care about a prospect's 40-yard dash once everything else about the player is known. Direct
your agent to:

1. Start from `data/nfl-combine-draft-2000-2018.csv`, one row per drafted player from the
   2000 to 2018 combines who ran the 40, 3,819 players, joined from the nflverse `combine` and
   `draft_picks` release files: draft year, name, Pro Football Reference id, combine position,
   school, height in inches, weight, 40 time, draft round, overall pick, drafting team, and his
   career since. `career_av` is Pro Football Reference's approximate value, a single number for
   a player's contribution over his career, weighted toward his best seasons. A player who
   never played an NFL game has an AV of 0. The draft classes stop at 2018 so that every player
   has had at least seven seasons to build a career.
2. Keep the offensive linemen (combine position OT, OG, C or OL) and the skill players (RB, WR
   and CB). Plot career AV against overall pick. Fit a straight line, then a curve with the pick
   and the pick squared, and use the curve to say what moving up from pick 15 to pick 5 is
   worth, and from pick 105 to pick 95.
3. Put every 40 on a fair scale. Linemen run about three quarters of a second slower than skill
   players, so build each player's 40 relative to his group: his time minus the average time
   for linemen, or for skill players.
4. Predict career AV from draft slot (the natural log of the pick bends the way the curve in
   step 2 does, and either one is fine), the relative 40, a lineman dummy, and the relative 40
   times the lineman dummy. Read what the 40 adds for a skill player once draft slot is in the
   model, and what it adds for a lineman.
5. Build an interactive scatter of career AV against overall pick, coloured by group, where
   hovering a point shows the player, school, drafting team and 40 time, and a control shows
   linemen only, skill players only, or both.
6. Commit the code and the output tables. `outputs/` again.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week06
```

That writes `weeks/week06/BRIEF.md` with both case studies' questions as headings and space
under each, eight in all. The brief is your thinking in your own words. Your code, tables, and
visuals are committed alongside it, so do not restate numbers the outputs already show; say
what they mean. Answer every question in a few sentences. `/coach-brief 6` will critique a
draft; it will not write one.

Each half has its own audience. Dombrowski is deciding how much money and how many years to
commit, so he needs to know what to expect from ages 30 to 34 and how sure you are. Beane is
deciding how his scouts rank players, so he needs to know where the 40 changes a decision and
where it does not.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, October 5 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
