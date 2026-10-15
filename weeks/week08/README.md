# Week 8: Data Collection and Cleansing

## Objectives

By Monday night you can:
- say what one row of a table is, and check a join by counting rows before and after it;
- tell a published download, an API and a scrape apart, and say what a source's terms let
  you do with its data;
- keep an API key out of your code, your commits and the chat;
- judge whether a data source can answer a question before you build anything on it.

## Thursday: recruiting to the draft (in class, in pairs, with Claude)

No worksheet this week. You work in Claude Code, in this repo, on one question: which college
programs turn recruiting into NFL draft picks, and which turn it into fewer than their
recruiting predicts? Two sources, joined by school.

### Before class

Register for a free key at `collegefootballdata.com/key`. It arrives by email, so do it the
night before. The free tier allows 1,000 calls a month; this lab uses about six.

### Set the key

1. Give Claude the CollegeFootballData documentation, or download the schema from the docs
   page and choose Use in Claude. Have it tell you how the API expects the key to be sent.
2. Using the documentation, have Claude create two files: `.env.example`, which names the
   variable `CFBD_API_KEY` with a placeholder value and gets committed, and `.env`, with the
   same line for you to fill in. Have it confirm `.env` is listed in `.gitignore`.
3. Open `.env` in your editor yourself and replace the placeholder with the key from your
   email. Save it.

Type the key into `.env` only. Never paste it into the chat, and never commit it. If it ever
ends up in a commit, get a new key from CollegeFootballData; deleting the commit does not
remove it from history.

### Direct your agent to

1. **Pull the recruiting rankings.** Point Claude at `api.collegefootballdata.com` and have it
   find the team recruiting endpoint and its fields before it writes any code. Then pull team
   recruiting rankings for the 2015 to 2020 classes, one call per class. The key is read from
   `.env`, never printed. Profile the pull: rows, columns, what one row is, and the share of
   blanks in each column. Plot the number of teams per class year.
2. **Download the draft picks.** nflverse publishes every NFL draft pick as one file, no key:
   `https://github.com/nflverse/nflverse-data/releases/download/draft_picks/draft_picks.csv`.
   Keep the 2018 to 2025 drafts. Save both raw pulls under `data/raw/` and leave them
   untouched. Profile the draft file the same way, then plot picks per draft year and compare
   each year with the official count (253 to 262 a year, compensatory picks included).
3. **Decide what one row is, and join by school.** Recruiting comes one row per program per
   class, and draft picks one row per player. Roll both up to one row per program, then join
   by school. The two sources do not spell schools the same way, so have Claude build a
   crosswalk, print every school that still does not match, and read the list yourself.
4. **Check the join.** Ask for these numbers, and save them to `outputs/`:
   - rows pulled from each source;
   - how many programs matched, and how many draft picks fell outside the join;
   - whether any program appears twice after the join;
   - rows before and after every filter and join, and why any were dropped.

   Also have Claude save a short note next to the raw files: where each came from, the date,
   and every change you made.
5. **Build a leaderboard of the programs that do the best at turning recruits into draft
   picks.** You decide what "best" means. Picks per class, raw picks, or picks against what
   a program's recruiting predicted (fit draft picks on recruiting points and look at the
   residual) are all options. Decide whether any recruiting classes are too early to call,
   since the 2020 class has only three drafts in this window. Save the leaderboard to
   `outputs/` and write down how you defined "best".

<details>
<summary>Stuck on the join?</summary>

- **Two spellings of one school.** nflverse writes "Ohio St." and "Miami (FL)". Find out how
  the recruiting data writes them, and map one to the other in the crosswalk.
- **Two schools that look alike.** "Delaware St." is not "Delaware", and "Miami (OH)" is not
  "Miami (FL)". A crosswalk that matches on part of a name gets these wrong without an error.
- **A fine drop or a bug?** A school with no recruiting ranking (FCS, Division II, a school
  outside the US) has nothing to join to, and that is coverage. A school with dozens of picks
  on the unmatched list is a bug.

</details>

### Submitting it

Commit the code Claude ran, the check numbers and the leaderboard in `outputs/`. They are
part of the Monday, October 19 submission. Out of time? Finish at home before you start the
Case Study. No need to ask.

## The Case Study (this repo, solo)

Two parts, one brief.

### Part 1: which programs produce NFL players?

You are writing to an NFL director of college scouting. Thursday's leaderboard says which
programs do the best at turning recruits into draft picks. A scouting department cares about
a second question: once a player is drafted, do players from some programs do better or worse
in the NFL than where they were picked?

**Direct your agent to:**

1. **Finish Thursday's leaderboard** if it is not done.
2. **Compare draft slot with career value.** The draft file carries `w_av`, Pro Football
   Reference's weighted career Approximate Value: one number for a player's NFL career that
   counts his best seasons most. Decide what a blank `w_av` means before you use it. Fit
   career value on draft pick, then compare each program's players with what their pick
   predicted.
3. **Group it two ways:** by program, and by type of program (conference, or Power 4 against
   Group of 5). CollegeFootballData's team list carries each program's conference. Decide
   which season's conference counts, and say so.
4. **Build one interactive view** of the comparison in a single HTML file in `outputs/`, open
   it in a browser, then ask Claude for one change you want.

<details>
<summary>Stuck on step 2?</summary>

- **Recent picks.** A player drafted in 2025 has had one season to build a career, so his
  `w_av` is small whatever his talent. Decide which drafts have had enough time, or compare
  each pick only with players from the same draft.
- **Small programs.** A program with three picks can top the list by luck. Decide how many
  picks a program needs before you rank it.
- **`car_av`** is in the file too, but check how many rows have it before you use it.

</details>

### Part 2: scouting the data for your final project

You are writing to the person who would act on your final project. No code is required.

1. **List two or three questions** your final project could answer, each with the person who
   would act on the answer.
2. **For each, search for data sources you could use.** Say what one row is, how you would
   collect it (download, API or scrape), what its terms allow, and what is missing.
3. **Pick the question with the best publicly available data** for a robust project.

Stay with Level I data: public box scores, published stats, public play-by-play. A project
that needs anything else is a conversation with the instructor first.

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week08
```

That writes `weeks/week08/BRIEF.md` with the five questions as headings, three for Part 1 and two for Part 2,
and space under each. The brief is your thinking in your own words. Your code, tables, and
visuals are committed alongside it, so do not restate numbers the outputs already show; say
what they mean. Answer every question in a few sentences. `/coach-brief 8` will critique a
draft; it will not write one.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

Check that `.env` is not in your commits: `git status` should never list it. Then `/audit`,
then `/quiz-me`. Submission = repo link in Canvas, Monday, October 19 at 11:59pm. You can
submit with items missing; anything missing at the deadline counts against the analysis half
of the grade.
