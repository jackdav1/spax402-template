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

## Thursday (in class, in Excel, no agentic AI)

Open `data/hand-build-rates-and-intervals-worksheet.xlsx`. It has three sheets, and every
highlighted cell on all three turns from yellow to green when the answer in it is right.
The check allows for rounding, so a value you rounded to three decimals still turns green.
Any yellow left anywhere in the file is work still to do.

Use cell references rather than typing numbers back in. A sheet built on references still
gives the right answer when a row changes, and you will change rows in the Case Study.

### Sheet 1, `field goals`

All 27 field goal attempts by Dustin Hopkins in the 2024 regular season and playoffs, one
row per kick, with the distance and the result. You compute his make rate, its standard
error, the 95% margin of error, both ends of the interval, and whether that interval
contains the league's make rate.

Three more cells cover the binomial. Two of them ask for the chance he makes his next two
kicks, once by multiplying his rate by itself in the formula bar and once with BINOM.DIST;
they should agree to every decimal, and when they do not, the BINOM.DIST arguments are in
the wrong order. The third asks BINOM.DIST for the chance a league-average kicker would
have made his number of kicks or fewer out of the same attempts, which asks how unusual
his season looks against the league's rate.

The same rows are in `data/hand-build-nfl-field-goals.csv` if you would rather build the
sheet from scratch.

### Sheet 2, `free throws`

Nick Anderson's 1994-95 season, and the four free throws he missed in a row in the closing
seconds of Game 1 of that year's Finals. You compute the chance a shooter at his season
rate misses all four, once by multiplying the miss rate by itself and once with
BINOM.DIST, and the chance he makes at least one.

The arithmetic is the easy half. Both routes assume the four attempts are independent of
each other and that his season rate is the right rate for those four attempts. Come to
class with an answer to which of those two you trust less.

### Sheet 3, `game log`

Kevin Durant's 2010-11 season, 78 games, with points and rebounds and assists for each
one. You compute the average, the standard deviation, the standard error, the relative
spread and both ends of the interval, for all three statistics.

This is the standard error of an *average*, not of a rate, which is why the individual
games have to be on the sheet at all: a rate hands you its own spread, an average does
not. COUNT, AVERAGE, STDEV.S and SQRT are the four functions you need. One last cell asks
how many standard errors sit between his scoring average and 30 points a game.

The same 78 games produced all three columns, so anything that differs between them is
the spread of the statistic and nothing else.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week02/data/`. All three
sheets are part of the Tuesday, September 8 submission, and sheet 1 is the number your
agent has to reproduce before you trust anything it computes for the whole league.

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
   average kicker would have made from the attempts each kicker actually faced. Turn that into
   an adjusted make rate for each kicker, on the same scale as his raw one, and compare the
   two rankings.
5. Check the table against what you already know before you write about it. The kicker
   attempts have to add up to the league total, every interval has to sit inside 0 and 1 or
   be flagged where it does not, and the adjusted rates have to average out to about the
   league rate. A table that fails one of those is wrong no matter how confident the agent
   sounds.
6. Commit the code you ran, plus the tables or charts that back up your brief. `outputs/` is
   the place for them.

A note on the last question in your brief. It is algebra on the margin of error formula
rather than a new method: fix the margin of error you need, then solve for the number of
attempts. Do it in Excel and show the number. Then compare it against how many field goals a
kicker actually attempts in a season, and say what that comparison means for the general
manager.

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
