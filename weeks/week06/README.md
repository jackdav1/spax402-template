# Week 6 — Regression Modeling Continued: Curves, Interactions, and Dummy Variables

## Objectives

By Monday night you can:
- decide whether a straight line, a curve, a dummy variable or an interaction fits the
  question, and say in words what each coefficient means;
- use a residual as a measure of how much a player beat what the model expected, and put it
  on a scale a coach can read;
- spot when the players still in a dataset are not the players who started in it, and fix
  the comparison.

## Thursday: the model lab (in class, with Claude)

No worksheet this week. You work in Claude Code, in this repo, on two files in `data/`:

- `nhl-skaters-2024-25.csv`: every NHL skater with at least 40 games in 2024-25, 600 players
  (397 forwards and 203 defensemen), from the NHL stats API. Points per game, average minutes
  on ice per game, goals, assists, shots, power-play points and a few more.
- `nba-players-2024-25.csv`: every NBA player with at least 40 games in 2024-25, 352 players,
  from Basketball-Reference. Points and minutes per game, usage rate (the percent of his team's
  possessions he ended while on the floor, stored as a percent: 18.9 means 18.9%), age,
  position, true shooting and a few more.

Every round has the same three steps.

1. **Predict.** Before you type a prompt, open `outputs/lab-predictions.md` and write two
   things yourself: the model as an equation (for example, points per game = a + b1 × minutes +
   b2 × minutes²), and your guess for the number that answers the round's question. Commit
   it. Nobody grades the guess. The commit shows it came first, and a wrong guess is where the
   learning happens.
2. **Build.** Have Claude fit the model, print the coefficient table, and build the round's
   interactive chart as a single HTML file in `outputs/lab/`. Open it in a browser.
3. **Break.** Push on it. Where is the model most wrong, and why? Ask Claude, then check its
   answer against the data.

### Round 1, the curve

NHL forwards only, 397 players. Points per game against minutes: a straight line, then a
curve (minutes and minutes squared). **Question:** over an 82-game season, how many points
does the 13th minute add, and how many does the 19th?

Build a scatter with both fits and a slider that picks a minute and shows what the next one
adds. Then break it: which forward beats the curve by the most, and which falls furthest
short? That gap is Tuesday's residual, used as a measure.

### Round 2, forwards and defensemen

All 600 skaters. Fit minutes plus a defenseman dummy (1 for a defenseman, 0 for a forward),
then add minutes times the dummy. **Question:** whose extra minute is worth more, a forward's
or a defenseman's, and by how much?

Build one chart with a line for each position and a toggle between the two models. Then
break it: compare the defenseman coefficient in the first model with the one in the second.
Why does it change so much?

### Round 3, minutes and usage

The NBA file. Fit minutes and usage, then add minutes times usage. **Question:** what is one
more minute worth to a player who uses 15% of his team's possessions, and to one who uses 30%?

Build a chart of points against minutes, with a usage slider that redraws the line. Then
break it: find a player the interaction model misses badly, and say what he does that the
model cannot see.

### Round 4, your interaction

Pick any two columns in either file that you think work together: one makes the other matter
more or less. Predict it, fit it, and chart it the same way. Keep it if it teaches you
something, including when it turns out to be nothing.

### Submitting it

Commit `outputs/lab-predictions.md`, the code Claude ran and the HTML files in `outputs/lab/`.
They are part of the Monday, October 5 submission. Out of time? Finish the rounds at home
before you start the Case Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: when do hitters peak?** You work for the Philadelphia Phillies. Dave
Dombrowski, the President of Baseball Operations, is weighing a five-year offer to a
30-year-old free agent hitter. He wants to know what the next five years of that bat are
likely to look like, and how sure you are.

### Before you open the data

Add three guesses to `outputs/prediction.md`, in your own words and without Claude, and
commit the file before you start:

1. The age at which hitters peak.
2. How much OPS a typical qualified 30-year-old hitter has lost by 34.
3. Out of every ten qualified 30-year-olds, how many are still qualified at 34.

### Direct your agent to

1. **Start from** `data/mlb-hitter-seasons-2008-2025.csv`, one row per player per season in
   which he batted at least once: 15,259 rows across seventeen seasons (2020's sixty-game
   season is left out), from the MLB Stats API. Columns: season, player id, name, birth date,
   age, games, plate appearances, at-bats, hits, doubles, triples, home runs, walks,
   strikeouts, hit by pitch, sacrifice flies, on-base percentage, slugging and OPS. Age is the
   player's age on June 30 of that season, the convention Baseball-Reference uses. Twenty
   names belong to more than one player, so follow hitters by player id, never by name.
2. **Fit the obvious curve.** Keep the qualified seasons, 300 or more plate appearances, for
   ages 21 to 38. Plot OPS against age. Fit a straight line, then a curve (add age squared),
   and find the age where the curve peaks. Look hard at what it says. If it does not match
   what you know about baseball, do not believe it yet.
3. **Find out what that curve is hiding.** Follow individual hitters instead of pooling them.
   What became of the hitters who were qualified at 30 by the time they were 34? When each
   hitter is compared only with himself a year earlier, what does aging look like, and at
   what age does the average change turn negative? Count a hitter's fate at 34 only when his
   age-34 season could be in the file: a hitter who was 30 in 2023 is 32 now, not gone, and
   nobody's age-34 season is 2020.
4. **Build the Contract Room.** Dombrowski picks any qualified hitter's age-30 season, in a
   single HTML file you commit and open in a browser. He sees:
   - the hitters who looked most like him at 30 (you decide what "most like" means, and say
     so on the page);
   - what happened to each of them over the next four seasons, with the ones who stopped
     being regulars or left the league drawn so he cannot miss them;
   - your projection for ages 31 to 34 from step 3.

   Hover shows each season. Your agent can build this in one pass, so ask for it directly.
   Then ask for one change you want.
5. **Your move.** Pick one thing you think changes the answer for a particular kind of hitter.
   Add your prediction to `outputs/prediction.md` and commit it, then test it. A few to start
   from, or bring your own:
   - power hitters (many home runs) against contact hitters;
   - high-strikeout hitters against low;
   - hitters who were regulars young against those who arrived late;
   - hitters from before 2015 against those after.
6. **Commit** the code you ran, plus the tables, charts and the Contract Room that back up
   your brief. `outputs/` is the place for them.

Ask any clarifying questions before you start.

<details>
<summary>Stuck on step 3?</summary>

- **Following hitters to 34.** Take each hitter qualified at 30 and look up his age-34 row:
  still qualified, batted but under 300 plate appearances, or no row at all.
- **Comparing a hitter with himself.** Pair each qualified season with the same player's
  season one year of age later, when he also qualified and the two seasons are consecutive
  in the file. 2019 and 2021 are two years apart, so they are not a pair. Average the change in OPS at each age, fit that change against age,
  and find where it crosses zero.
- **Then compare.** Put the qualified 30-year-olds who were still qualified at 34 beside the
  ones who were not, using their OPS at 30.

</details>

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week06
```

That writes `weeks/week06/BRIEF.md` with the four questions as headings and space under each.
The brief is your thinking in your own words. Your code, tables, and visuals are committed
alongside it, so do not restate numbers the outputs already show; say what they mean. Answer
every question in a few sentences. `/coach-brief 6` will critique a draft; it will not write
one.

Dombrowski is deciding how much money and how many years to commit. He needs to know what to
expect from ages 30 to 34, and how sure you are.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, October 5 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
