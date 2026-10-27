# Week 10: Cognitive Biases in Sports

## Objectives

By Monday night you can:
- name the cognitive bias behind a real sports decision or take, and tell it apart from the
  biases next to it (recency or hot hand, outcome or hindsight);
- test a claim with data instead of looking for data that agrees with it;
- make the strongest case for the decision you are arguing against, and say whether your data
  answers it.

There is no lab this week. Tuesday and Thursday are both lecture, and the Case Study is the
week's work.

## The Case Study (this repo, solo)

Find a decision or article from the 2025 or 2026 season in which at least one cognitive bias
shows. Coach decisions, contract decisions, award votes and media takes on a hot streak are all
fair game. Then argue against it with data.

Public data only: nflverse, Baseball Savant, Basketball Reference, the NCAA stats site and
similar.

**Direct your agent to:**

1. **Find the data that tests the claim.**

   > Here is the decision (or article) I'm testing: [link]. It claims [the claim]. Find public
   > data that would show whether it holds up. I want a test, not support, so tell me what
   > result would prove the decision right.

   Watch the wording. Asking Claude to find data that supports your argument gets you a yes
   every time; that is confirmation bias with a faster search.

2. **Build one interactive chart that makes your argument.** Save it in `outputs/`.

3. **Commit the code, the chart and a link to the decision or article** (in
   `outputs/source.md`).

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week10
```

That writes `weeks/week10/BRIEF.md` with the three questions as headings and space under each.
The brief is your thinking in your own words, half a page to a page. Your chart is committed
alongside it, so do not restate what it shows; say what it means for the decision. `/coach-brief
10` will critique a draft; it will not write one.

## Final project proposal

Also due Thursday, November 5, in Canvas: your research question, the strategies you would use to
answer it, your data sources, and the challenges you expect. If your project needs data that
isn't public, talk to Jack before you start.

## Before you push

Commit your code, your chart and your link. Then `/audit`, then `/quiz-me`. Submission = repo
link in Canvas, Monday, November 2 at 11:59pm. You can submit with items missing; anything
missing at the deadline counts against the analysis half of the grade.
