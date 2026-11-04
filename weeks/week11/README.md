# Week 11: Simulations

## Objectives

By Monday night you can:
- say what a Monte Carlo simulation does: play the uncertain thing many times with odds you
  chose, then count what happened;
- turn team ratings into win probabilities and check them against games already played;
- read a table of simulated odds and name the input most likely to break it.

There is no class on Tuesday (Election Day). Thursday is the week's only class, and the Case
Study is the week's work.

## The Case Study (this repo, solo)

Pick one season that is happening right now, simulate the rest of it 10,000 times, and
commit predictions that will mostly resolve before the semester ends.

The data is already in `weeks/week11/data/`, pulled on Wednesday, November 4. Each sport has
two files with the same columns, `<sport>_played.csv` (games with scores) and
`<sport>_remaining.csv` (games still to play), plus `<sport>_rules.md`, which explains the
playoff format and the shortcuts you may take. Pick one:

- **NFL 2026 (`nfl`):** the seven playoff seeds in each conference, then the Super Bowl.
- **NBA 2026-27 (`nba`):** the top six and the play-in in each conference, then the title.
- **NHL 2026-27 (`nhl`):** division spots and wild cards, then the Stanley Cup.
- **College football 2026 (`cfb`):** which two teams reach each conference title game, and
  who wins it.
- **Premier League 2026-27 (`epl`):** the title, the top four and the three relegation places.

`pull_week11_data.py` is the script that pulled the files. You don't need to run it.

**Direct your agent to:**

1. **Load your sport's played and remaining games.** Read `<sport>_rules.md` first, and
   check that the standings you compute from the played games match the league's.

2. **Give each team a rating from its results.** Point or goal differential per game is
   enough. Turn a rating difference into a win probability, with an advantage for the home
   team. Then check it on the games already played: when the model said 70%, did those teams
   win about 70% of the time?

3. **Simulate the rest of the season and the postseason 10,000 times.**

   > Using my ratings and win probability model, simulate every remaining game, then the
   > postseason in `<sport>_rules.md`, 10,000 times. Count how often each team makes the
   > playoffs, wins each round and wins the title.

4. **Report each team's odds in a table**, saved in `outputs/`.

5. **Build an interactive page with a slider** that changes one input, such as one team's
   rating or the size of home advantage, and updates the odds. Save it in `outputs/`.

6. **Commit your predictions as `weeks/week11/predictions.csv`**, one row per team with the
   odds from your table. Most of them resolve before the semester ends, so you will find out
   how you did.

You can simulate a different sport or league that is in season, but it takes more time: you
find the data, write the rules file and check the standings yourself. The data has to be
public.

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week11
```

That writes `weeks/week11/BRIEF.md` with the three questions as headings and space under each.
The brief is your thinking in your own words. Your odds table and page are committed alongside
it, so do not restate what they show; say what you believe about them and why. Answer every
question in a few sentences. `/coach-brief 11` will critique a draft; it will not write one.

## Before you push

Commit your code, your odds table, your interactive page and `predictions.csv`. Then `/audit`,
then `/quiz-me`. Submission = repo link in Canvas, Monday, November 9 at 11:59pm. You can
submit with items missing; anything missing at the deadline counts against the analysis half
of the grade.
