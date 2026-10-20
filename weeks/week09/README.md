# Week 9: Data Storytelling

## Objectives

By Monday night you can:
- name the one thing an audience should take away, and say what you left out to get there;
- tell a story as a problem, the evidence that reinforces it, and a solution;
- pick the medium (one-pager, deck, video) that fits how your audience will use it;
- write a skill that makes Claude follow your rules by default, and fix the skill when its
  output is wrong.

## Thursday: write a skill and test it (in class, with Claude)

A skill is a file of instructions Claude loads when the task calls for it. It lives in its own
folder as `SKILL.md`: a name, a description that says when to use it, and a body that says how.
You have used skills all semester (`/update`, `/audit`, `/quiz-me`). This week you write one.

Your skill goes in `.claude/skills/viz-story/SKILL.md`, next to the course skills. Claude Code
only loads skills from `.claude/skills/`. `/update` only ever changes the six course skills
(audit, coach-brief, quiz-me, submit, teach, update), so a skill you write there is yours and
stays put.

### Direct your agent to

1. **Write the skill with Claude.**

   > Interview me one question at a time about how I want charts and one-pagers made for a
   > coach or front office: audience, takeaway, chart form, color, clutter, and AI tells to
   > avoid. Then save it as a skill called viz-story.

   Push past vague answers. "Make it clean" is not a rule; "no gridlines, label lines where
   they end, one highlight color" is.

2. **Run it on your Week 8 leaderboard.**

   > Use my viz-story skill to rebuild my Week 8 leaderboard chart for an NFL general manager
   > or a college recruiting director. Save the old and new versions side by side.

3. **Check it against your own rules.**

   > Review the new chart against every rule in my viz-story skill and make sure it complies.
   > If needed, fix the skill along with the chart.

When the output is wrong, fix the instruction, not just the chart. A chart fixed by hand stays
fixed once; a rule fixed in the skill stays fixed every time.

Commit the skill and both versions of the chart. Out of time? Finish at home before you start
the Case Study.

## The Case Study (this repo, solo)

One story told twice, from your Week 8 leaderboard, to one audience you pick: an NFL team's
general manager or a college team's recruiting director (your choice of team). The GM wants to
know which programs' players to trust on draft day. The recruiting director wants to know where
their program stands as a developer of NFL players, and what to say to recruits.

**Direct your agent to:**

1. **Build a one-pager or a three-slide deck** for your audience from your Week 8 leaderboard,
   using your viz-story skill. Save it in `outputs/`.
2. **Write a 60 to 90 second narration script** that tells the same story: the problem, the
   evidence that reinforces it, and the solution. Save it in `outputs/`.
3. **Turn it into a video** with your recorded voice narrating it. Slides with your voice over
   them are a fine video.
4. **Update your skill** with anything you had to fix by hand.

<details>
<summary>Stuck on the script?</summary>

- **Write it the way you talk.** Contractions, short sentences, one idea per line.
- **Say the number, then what it means.** "Twelve picks from three recruiting classes" lands;
  "a residual of plus 4.2" does not.
- **Don't describe the screen.** The visual shows the chart; your voice says the point.

</details>

## Your brief (BRIEF.md, typed by you)

Create it once, then answer the questions in it:

```
python3 scripts/new_brief.py week09
```

That writes `weeks/week09/BRIEF.md` with the three questions as headings and space under each.
The brief is your thinking in your own words. Your one-pager, script and skill are committed
alongside it, so do not restate what they show; say why you made the choices you made. Answer
every question in a few sentences. `/coach-brief 9` will critique a draft; it will not write
one.

## Before you push

Commit your skill (`.claude/skills/viz-story/`), your one-pager or deck, your script and your
video. A video over GitHub's 100 MB file limit gets committed as a link instead (a OneDrive or
YouTube link in `outputs/video.md`). Then `/audit`, then `/quiz-me`. Submission = repo link in
Canvas, Monday, October 26 at 11:59pm. You can submit with items missing; anything missing at
the deadline counts against the analysis half of the grade.
