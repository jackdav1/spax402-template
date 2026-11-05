# Week 12: Introduction to Machine Learning Models

## Objectives

By Monday night you can:
- say what a decision tree and a random forest do, and direct an agent to build one;
- judge a model on data it never saw, and say when it has overfit;
- read a confusion matrix and choose between accuracy, precision and recall for a decision;
- catch data leakage: a column the model would not have when it makes the prediction.

## Thursday: the model lab (in class, with Claude)

No worksheet this week. You work in Claude Code, in this repo, on one file:
`weeks/week12/data/nfl-field-goals-2016-2025.csv`, every NFL field goal attempt from 2016 to
2025, regular season and playoffs, 10,015 of them, from nflverse play-by-play. One row is one
kick. Columns: game id, season, regular season or playoffs, week, kicking team, opponent,
whether the kicking team was at home, the kicker's name and id, the kick distance in yards,
quarter, seconds left in the game, the kicking team's score minus the opponent's, whether the
game was indoors (a dome or a closed roof), grass or turf, wind in miles per hour, the result
(made, missed or blocked) and `made` (1 if it was good, 0 if not). Wind is 0 indoors. Kicks
from games with an open retractable roof or no recorded wind are left out.

Each round is the same three steps:

1. **Predict.** Before any prompt, write your guess for the round's number in
   `outputs/lab-predictions.md` and commit it.
2. **Build.** Have Claude build the model. Use a train/test split of 0.8/0.2 and report
   everything on the test kicks.
3. **Break.** Find where the model is wrong, and say why.

### Round 1: every kick is good

A model that says every field goal is good. How often is it right on the test kicks? How many
misses does it catch?

### Round 2: distance

A decision tree classifier with a maximum depth of two, on kick distance alone. Show a
confusion matrix of the test kicks, with totals and with percentages. How many misses does it
catch?

### Round 3: class weights

The same tree, with balanced class weights. Now how many misses does it catch, and how often is
it right when it predicts a miss? At what distance does it start predicting misses?

### Round 4: the kickers

Add the kicker's name, one-hot encoded, plus wind and indoors, and let the tree grow with no
depth limit. Guess its accuracy on the kicks it learned from and on the test kicks before you
run it.

### Round 5: your model

Build the model you would hand a coach deciding whether to attempt a kick. Pick the goal you
optimize for, and say why. Then make it land: an interactive page where the coach sets the
distance and the conditions and sees what your model says. Save it as a single HTML file in
`outputs/lab/`, open it in a browser, then ask Claude for the one change that makes it clearer.

### Submitting it

Commit `outputs/lab-predictions.md`, the code Claude ran and the HTML file in `outputs/lab/`.
They are part of the Monday, November 16 submission. Out of time? Finish at home before you
start the Case Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: 4th & 1.** Your head coach is evaluating his offensive 4th & 1 strategy from all
field positions. He wants to know which approaches tend to result in first downs at the highest
rate.

### Before you open the data

Add your guess to `outputs/prediction.md`, in your own words and without Claude, and commit it
before you start: which 4th & 1 play call converts most often, and about how often?

### Direct your agent to

1. **Start from** `weeks/week12/data/nfl-fourth-and-one-2016-2025.csv`, every NFL 4th & 1
   run or pass from 2016 to 2025, regular season and playoffs, 2,689 plays, from nflverse
   play-by-play joined to nflverse participation data. Plays with a penalty are left out. One
   row is one play. Columns:
   - `game_id`, `play_id`, `season`, `week`, `offense`, `defense`, and `home` (1 if the
     offense was the home team);
   - `yardline_100`, yards from the opponent's end zone, so 1 is 4th & goal from the 1;
   - `qtr`, `game_seconds_remaining` and `score_differential` (the offense's score minus the
     defense's);
   - `drive_result`, how the drive ended;
   - `roof` and `surface`;
   - `play_call`, run or pass. A designed pass is a pass even if the quarterback scrambled;
   - `qb_sneak`, 1 when the quarterback ran it from under center;
   - `run_direction`, left, middle or right for a run, and `pass` for a pass;
   - `shotgun` and `no_huddle` (1 or 0);
   - `offense_formation`, `offense_personnel`, `defenders_in_box` and `defense_personnel`;
   - `converted`, 1 if the offense got the first down and 0 if not. This is the target.
2. **Write your prompt before you run anything.** Save it as `outputs/prompt.md` and commit it.
   Fill in each of the six parts:
   - the target variable;
   - the goal of the model;
   - the model and its settings: a decision tree classifier with a maximum depth of two or
     three, and a train/test split of 0.8/0.2;
   - the transformations it needs: the text columns have to be one-hot encoded;
   - how you will judge it: a labeled confusion matrix of the test plays, with totals and with
     percentages, and the goal you optimize for, balancing class weights if needed;
   - the visuals you want: the tree, drawn.
3. **Run it, and compare it with a baseline:** a model that says every 4th & 1 converts.
4. **Read the tree.** Turn its top splits into advice your coach could use, and check each one
   against the plays themselves: how many plays sit behind the split, and how often they
   converted.
5. **Build an interactive page** where the coach picks a situation (field position, formation,
   play call) and sees what your tree predicts and how often similar plays converted. Save it
   in `outputs/`.
6. **Commit** the code you ran and the tables, charts and page that back up your brief.

Ask any clarifying questions before you start.

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week12
```

That writes `weeks/week12/BRIEF.md` with the four questions as headings and space under each.
The brief is your thinking in your own words. Your code, tables and page are committed
alongside it, so do not restate what they show; say what they mean. Answer every question in a
few sentences. `/coach-brief 12` will critique a draft; it will not write one.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, November 16 at 11:59pm.
You can submit with items missing; anything missing at the deadline counts against the
analysis half of the grade. Exam #2 is Thursday, November 19.
