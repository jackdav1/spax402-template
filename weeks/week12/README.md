# Week 12: Introduction to Machine Learning Models

## Objectives

By Monday night you can:
- say what a decision tree and a random forest do, and direct an agent to build one;
- judge a model on data it never saw, and say when it has overfit;
- read a confusion matrix and choose between accuracy, precision and recall for a decision;
- check whether a model's probabilities mean what they say (calibration and the Brier score);
- catch data leakage: a column the model would not have when it makes the prediction.

## Thursday: the model lab (in class, with Claude)

No worksheet this week. You work in Claude Code, in this repo, on one file:
`weeks/week12/data/nfl-field-goals-2016-2025.csv`, every NFL field goal attempt from 2016 to
2025, regular season and playoffs, 10,015 of them, from nflverse play-by-play. One row is one
kick. Kicks from games with an open retractable roof or no recorded wind are left out. Every
column except the last two is known before the kick:

- `game_id`, `season`, `season_type` (regular or playoffs), `playoff` (1 for a playoff game),
  `week`, `kicking_team`, `opponent`, and `home` (1 if the kicking team was at home);
- `stadium` and `stadium_id`, as nflverse records them (a team's stadium can change names, so
  use the id to group), and `denver_altitude` (1 for kicks in Denver's stadium);
- `kicker` and `kicker_id`;
- `kicker_prior_attempts` and `kicker_prior_rate`: how many field goals this kicker attempted
  before this kick, from 2016 on, and the share of them he made (0 to 1). Only earlier kicks
  count, never this one or later ones. Blank for a kicker's first kick in the file;
- `kick_distance` in yards, `qtr`, `game_seconds_remaining`, and `score_differential` (the
  kicking team's score minus the opponent's);
- `iced`, 1 when the defense called a timeout right before the kick, with no snap in between;
- `roof` (outdoors, dome or closed), `indoor` (1 for a dome or a closed roof) and `surface`
  (grass or turf);
- `wind` in miles per hour (0 indoors) and `temp` in degrees Fahrenheit (blank indoors: nflverse
  doesn't record a temperature under a roof);
- `precipitation`, 1 when the game's weather note mentions rain, snow, showers, drizzle, sleet,
  flurries or storms. Forecast phrases such as "chance of rain" don't count;
- `result` (made, missed or blocked) and `made` (1 if it was good, 0 if not). These two are the
  outcome.

Public play-by-play doesn't record which hash the ball was spotted on, so the file has no hash
mark column.

In class, Jack walks through example models on this file and what each one gets wrong. Then
it's your turn.

### Your model

Build the best model you can for the probability that a field goal is good. Train on 2016 to
2023 and test on 2024 and 2025, so the test kicks come after every kick the model learns from.
Which columns and which model are up to you.

1. **Set a `/goal` first.** `/goal` sets a finish line: after every turn a second model reads
   the conversation and decides whether the condition holds. It can't run code or open files,
   so every clause has to be something Claude's output will show. Give it a concrete success
   condition and a turn cap, such as `or stop after 15 turns` (there is no limit unless you
   write one). Save it as `outputs/lab/goal.md` and commit it before you run it.
2. **Report on the 2024 and 2025 kicks:** accuracy next to a model that says every kick is
   good, the Brier score (the average squared gap between the predicted probability and what
   happened; lower is better), and a calibration chart (predicted probability against how often
   those kicks were good). Save the chart in `outputs/lab/`.
3. **Write two sentences** in `outputs/lab/goal.md`, under your goal, on what you'd tell a
   kicking coach.

`/goal` with nothing after it shows the status, and `/goal clear` stops it. A goal doesn't
change your permissions: unless you switch to auto mode, Claude still stops to ask before it
runs code, so stay at the keyboard and approve each step. When it finishes, check the output
against each clause of your goal yourself.

### Submitting it

Commit `outputs/lab/goal.md`, the code Claude ran and the calibration chart in `outputs/lab/`.
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
   Cover each of the five parts from the lecture:
   - your question and audience;
   - how you define success (ask an LLM to grill you on edge cases);
   - what data you have available and want to use: where it lives, what one row is, what the
     columns mean, and when each one becomes known;
   - what you want to optimize for, including which mistake costs more;
   - what to watch out for, such as a column known only after the snap.
3. **Run it, and compare it with a baseline:** a model that says every 4th & 1 converts. The
   model is a decision tree classifier with a maximum depth of two or three and a train/test
   split of 0.8/0.2. Show a labeled confusion matrix of the test plays, with totals and with
   percentages, and the tree, drawn.
4. **Check its probabilities.** Have the model report a predicted conversion probability for
   each test play. Show a calibration chart of the test plays (predicted probability against
   how often those plays converted; five bins, since there are only about 540 test plays) and
   the Brier score, next to the Brier score of a baseline that gives every play the league
   conversion rate from the training plays.
5. **Read the tree.** Turn its top splits into advice your coach could use, and check each one
   against the plays themselves: how many plays sit behind the split, and how often they
   converted.
6. **Build an interactive page** where the coach picks a situation (field position, formation,
   play call) and sees what your tree predicts and how often similar plays converted. Save it
   in `outputs/`.
7. **Commit** the code you ran and the tables, charts and page that back up your brief.

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
