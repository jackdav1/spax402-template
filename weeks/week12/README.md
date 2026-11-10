# Week 12: Introduction to Machine Learning Models

## Objectives

By Monday night you can:
- say what a decision tree and a random forest do, and direct an agent to build one;
- judge a model on data it never saw, and say when it has overfit;
- read a confusion matrix and choose between accuracy, precision and recall for a decision;
- check whether a model's probabilities mean what they say (calibration and the Brier score);
- catch data leakage: a column the model would not have when it makes the prediction.

## The Case Study: field goals (Thursday in class, then solo)

No worksheet this week. You start in class on Thursday and finish on your own. You work in Claude Code, in this repo, on one file:
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
you build your own, which is this week's Case Study.

### Before you open the data

Add your guess to `outputs/prediction.md`, in your own words and without Claude, and commit it
before you start: how often is a 54 yard field goal good, and how much does rain change that?

### Your model

Build the best model you can for the probability that a field goal is good. Train on 2016 to
2023 and test on 2024 and 2025, so the test kicks come after every kick the model learns from.
Which columns and which model are up to you.

1. **Set a `/goal` first.** `/goal` sets a finish line: after every turn a second model reads
   the conversation and decides whether the condition holds. It can't run code or open files,
   so every clause has to be something Claude's output will show. Give it a concrete success
   condition, such as a target score, and a turn cap, such as `or stop after 15 turns` (there
   is no limit unless you write one). Save it as `outputs/lab/goal.md` and commit it before
   you run it.
2. **Report on the 2024 and 2025 kicks:** accuracy next to a model that says every kick is
   good, the Brier score next to a baseline that gives every kick the training make rate
   (lower is better), and a calibration chart (predicted probability against how often those
   kicks were good). Save the chart in `outputs/lab/`.
3. **Build an interactive page** where a coach sets up a kick (distance, weather, the kicker's
   record, the game situation) and sees your model's probability that it's good. Save it in
   `outputs/`.
4. **Commit** the code you ran and the tables, charts and page that back up your brief.

`/goal` with nothing after it shows the status, and `/goal clear` stops it. A goal doesn't
change your permissions: unless you switch to auto mode, Claude still stops to ask before it
runs code, so stay at the keyboard and approve each step. When it finishes, check the output
against each clause of your goal yourself.

Out of time in class? Finish at home. No need to ask.

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week12
```

That writes `weeks/week12/BRIEF.md` with the two questions as headings and space under each.
The brief is your thinking in your own words. Your code, tables and page are committed
alongside it, so do not restate what they show; say what they mean. Answer every question in a
few sentences. `/coach-brief 12` will critique a draft; it will not write one.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, November 16 at 11:59pm.
You can submit with items missing; anything missing at the deadline counts against the
analysis half of the grade. Exam #2 is Thursday, November 19.
