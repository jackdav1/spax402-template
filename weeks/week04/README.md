# Week 4 — Descriptive and Probabilistic Statistics in Sports

## Objectives

By Monday night you can:
- classify a statistic as counting, efficiency, weighted efficiency or probabilistic, and
  say what each kind leaves out;
- name the inputs of a probabilistic statistic, say what it is optimizing for, and say when
  a team should stop optimizing for it;
- put two statistics on the same scale with z-scores and explain why they disagree about a
  play.

## Thursday (in class, in Excel, no agentic AI)

Open `data/hand-build-descriptive-worksheet.xlsx`. It has three sheets. The given numbers sit
in the left-hand columns, your answers go in the yellow cells, and the gray Check cell beside
each answer turns green when the answer is right. The check allows for rounding, so a value you
rounded to three decimals still turns green. Any gray left in a Check column is work still to
do.

Use cell references rather than typing numbers back in. Every rate on these sheets is a ratio
of cells that are already there, and a sheet built on references lets you change one given
value and watch everything below it move.

### Sheet 1, `four factors`

The box score from Indiana Fever at Los Angeles Sparks, August 29, 2025, a one-point game.
Los Angeles is in column B and Indiana in column C: points, field goals made and attempted,
three-pointers made, free throws made and attempted, offensive and defensive rebounds, and
turnovers. The free throw possession weight, 0.44, is a given cell of its own.

For each team you compute Dean Oliver's Four Factors: effective field goal percentage,
free throw attempt rate, turnover percentage and offensive rebound percentage. Then
possessions, estimated as FGA - ORB + TOV + 0.44 x FTA, and points per possession. Offensive
rebound percentage needs the opponent's defensive rebounds, so each team's block reads from
both columns. Los Angeles's block is first and Indiana's is below it.

Los Angeles shot much better from the field and lost. Work out which factor made up the
difference, and by how much. Tuesday's deck works a different game, so it will not tell you.

### Sheet 2, `weighted efficiency`

Jonathan India, Ceddanne Rafaela and Shea Langeliers, 2024 season totals: at bats, hits,
doubles, triples, home runs, walks, intentional walks, hit by pitches and sacrifice flies.
They sit in columns B, C and D. The six wOBA weights are given below the stat lines.

Singles are not on a stat line, so they come first: hits minus doubles, triples and home
runs. Then batting average, on-base percentage, slugging (weights 1, 2, 3 and 4 on the four
hit types, over at bats), OPS, unintentional walks (BB - IBB), the wOBA numerator and
denominator, and wOBA itself. SUMPRODUCT does the weighted sums in one cell each.

Rank the three hitters by average, by OPS and by wOBA. The three rankings do not agree. Two
of these three had the same season by average and by slugging, so decide what wOBA's extra
work bought you that OPS did not, and whether it was worth it.

### Sheet 3, `epa and wpa`

Twelve plays from Baltimore at Buffalo, Week 1 of the 2025 season, Buffalo 41 and Baltimore
40, with each play's expected points added and win probability added from nflverse. The score
each play was run at is given beside it. The twelve were chosen so the two statistics
disagree about several of them. For each play you compute the z-score of its EPA and of its
WPA with STANDARDIZE, using AVERAGE and STDEV.S over the twelve plays, then the difference
between the two z-scores. Two cells at the bottom ask for the correlation between EPA and WPA
across the twelve, with CORREL, and the largest absolute gap.

Tuesday's deck works Super Bowl LI. This game is on no slide. Find the two largest gaps in
either direction, look at the score column beside them, and say what they have in common.

STANDARDIZE takes the value, the mean and the standard deviation, in that order. Compute the
mean and standard deviation once each and point every row at those cells.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week04/data/`. All three
sheets are part of the Monday, September 21 submission.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: what decided Super Bowl LX?** You work for a head coach. Seattle beat New
England 29 to 13, and the coach wants to know which plays decided it and whether the two
numbers the analytics staff keep quoting, EPA and WPA, agree. Direct your agent to:

1. Start from `data/super-bowl-lx-plays.csv`. It is every play of the game from the nflverse
   play-by-play release for the 2025 season: quarter, clock, offense and defense, down and
   distance, yard line, score differential, play type, the play description, EPA, WPA and the
   offense's win probability before the play. Nothing outside this game is in the file, and
   nothing outside it belongs in your analysis. The same rows are in the public
   `play_by_play_2025` parquet on the nflverse GitHub releases page if you want to check one.
2. Plot every play's EPA against its WPA and compute the correlation.
3. Standardize both columns with z-scores, take the difference, and find the plays where the
   two statistics disagree most. The inputs to the two models are on the Tuesday deck; the
   one input WPA has and EPA does not is where every large gap comes from.
4. Build an interactive win probability chart of the game: the offense's win probability
   before every play across all four quarters, where hovering a point shows the play
   description, its EPA and its WPA, and the plays from step 3 are marked. A single HTML
   file is enough; commit it and open it in a browser. Your agent can build this in one
   pass, so ask for it directly.
5. Build a counting statistic and an efficiency statistic from the same data that tell two
   different stories about a team or a player in this game.
6. Commit the code you ran, plus the tables, charts, and visuals that back up your brief.
   `outputs/` is the place for them.

EPA and WPA are nflfastR's models, from the offense's point of view on every play. A
negative EPA on a defensive play means the offense lost expected points, which is the
defense's gain.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week04
```

That writes `weeks/week04/BRIEF.md` with this week's questions as headings and space under
each. The brief is your thinking in your own words. Your code, tables, and visuals are
committed alongside it, so do not restate numbers the outputs already show; say what they
mean. Your audience is a head coach, so he needs to know which play to show on film and
which number to trust late in a close game, not what a z-score is. Answer every question in
a few sentences. `/coach-brief 4` will critique a draft; it will not write one.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, September 21 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
