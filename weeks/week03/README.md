# Week 3 — Beyond Statistical Significance: Bayes' Theorem

## Objectives

By Tuesday night you can:
- differentiate between “how surprising the data is if nothing changed” and “the
  likelihood that something did change”, and say which one a p-value answers;
- identify conditions where prior beliefs should be included in analysis, then quantify
  those prior beliefs and factor them in using Bayes' theorem.

## Thursday (in class, in Excel, no agentic AI)

Open `data/hand-build-bayes-worksheet.xlsx`. It has three sheets. On each one the given
numbers sit in column B, your answers go in the yellow cells in column E, and the gray Check
cell beside each answer turns green when the answer is right. The check allows for rounding,
so a value you rounded to three decimals still turns green. Any gray left in a Check column
is work still to do.

The Check cells are new this week. In Week 2 the check lived on the answer cell itself, and a
formula copied from one answer cell into the next carried the wrong check along with it. Now
the check watches the answer from beside it, so copy and paste as much as you like.

Use cell references rather than typing numbers back in. Every posterior on these sheets is
the same formula, prior times likelihood over the total, and a sheet built on references lets
you change the prior and watch the answer move.

### Sheet 1, `hot start`

LaMonte Wade Jr. hit .333 in April 2024, 21 for 63, against a career .241 over 1,077 at
bats. You compute the p-value for an April that good if he is still a .241 hitter, then the
likelihood of 21 for 63 if he is a .300 hitter and the likelihood if he is his career self,
both with BINOM.DIST. The posterior uses the base rate from Tuesday's deck as the prior. A
last cell asks for the same posterior at a 20% prior, so you can see how much of the answer
is the April and how much is the prior.

### Sheet 2, `free throws`

Nick Anderson again. Last week you computed how unlikely four straight misses were for a
70.4% shooter. This week you ask the question you wanted to ask then: how likely is it that
he choked? A player who chokes is defined on the sheet as a 50% shooter from the line. You
compute the likelihood of four misses under each hypothesis, their ratio, and the posterior.

Cell B7 is your prior, the chance a player in that spot chokes, before the misses. There is
no check on it because there is no right answer. Pick a number, write down why, and be ready
to say whether the four misses moved you. The posterior cell checks against whatever prior
you chose.

### Sheet 3, `yards per carry`

Christian McCaffrey averaged 3.10 yards a carry through week 5 of 2025, on 91 carries,
against a career 4.83 with a standard deviation of 7.40 yards per carry. You compute the
standard error of his early average, the z score, and the p-value with NORM.DIST, which is
the Week 2 computation. Then the two likelihoods, also with NORM.DIST, at his career average
and at a full yard below it, and the posterior on the football base rate from the deck.

The fourth argument of NORM.DIST changes what the function returns. TRUE is the area to the
left of x, which is the p-value. FALSE is the height of the curve at x, which is the
likelihood. The same function answers both questions, which is the whole point of the week.

### Submitting it

Commit the filled-in worksheet where it already sits, in `weeks/week03/data/`. All three
sheets are part of the Monday, September 14 submission, and sheet 1 is the computation your
agent has to reproduce for one hitter before you trust it on the whole league.

Need more time? Finish the hand-build at home Thursday evening, before you start the Case
Study. No need to ask.

## The Case Study (this repo, solo)

**Case Study: is Jorge Polanco's April real?** You work for the Seattle Mariners, and the
manager wants to know whether Polanco's .384 April, 28 for 73, means he is a different hitter
than his career .263 says. Every April somebody hits .380, and most of them are back at their
career average by June. Your job is to say how much this one should move the manager, and to
do the same for everyone else who started hot. Direct your agent to:

1. Start from `data/april-2025-hot-starts.csv`. It has every hitter with at least 1,000
   career at bats entering 2025 and at least 50 at bats in April 2025: his April hits and at
   bats, and his career hits and at bats from 2010 through 2024. Nothing after April 30,
   2025 is in the file, and nothing after April 30 belongs in your analysis. The file came
   from the MLB Stats API; the `people/{id}/stats` endpoint with `season` and `byDateRange`
   returns the same totals if you want to check one.
2. Compute the prior. The deck's base rate counted how often an established hitter at .265
   or under became a .300 hitter over a full season, 2015 through 2024. Use that number, or
   compute your own from data you can name, and say where it came from.
3. For Polanco, compute the two likelihoods with the binomial distribution, one for a .300
   hitter and one for his career average, and the posterior. Then run the same computation
   on every hitter in the file who hit .300 or better in April.
4. Show how the answer moves with the prior, at 1% and at 50% as well as the base rate.
5. Make one chart that shows why the same April average is stronger evidence for one hitter
   than for another. Career average and April at bats are the two things that differ.
6. Commit the code you ran, plus the tables or charts that back up your brief. `outputs/`
   is the place for them.

## Your brief (BRIEF.md — typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week03
```

That writes `weeks/week03/BRIEF.md` with this week's questions as headings and space under
each. Your audience is a manager, so he needs to know whether to move Polanco up in the order,
not what a likelihood is. Answer every question in a few sentences, in your own words.
`/coach-brief 3` will critique a draft; it will not write one.

The same questions scope the analysis, not just the write-up. If an output answers none of
them, it is off-target; if a question has no output behind it, that is the gap to fix before
you push.

## Before you push

`/audit`, then `/quiz-me`. Submission = repo link in Canvas, Monday, September 14 at
11:59pm. You can submit with items missing; anything missing at the deadline counts against
the analysis half of the grade.
