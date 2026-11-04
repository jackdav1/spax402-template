# Premier League 2026-27: title, top four and relegation

Snapshot taken Wednesday, November 4, 2026, from fixturedownload.com. `epl_played.csv` has
the 90 matches played through Monday, November 2 (nine per team). `epl_remaining.csv` has the
other 290. Every team plays the other 19 twice, home and away, for 38 matches. Team names are
fixturedownload's short names, such as "Man Utd", "Spurs" and "Nott'm Forest".

## How the table works

- A win is 3 points, a draw 1, a loss 0.
- Teams are ranked by points, then goal difference, then goals scored.
- There are no playoffs. The team on top after 38 matches wins the title.

## What gets simulated

- The title: first place.
- Top four: the Champions League places. England can earn a fifth place through how its
  clubs do in Europe; ignore that and simulate the top four.
- Relegation: the bottom three (18th, 19th and 20th) go down.

## Draws

Draws are common in the Premier League, so a model that only picks a winner will be wrong in
a way that matters for points. Your model needs a chance of a draw. Two simple ways: simulate
each team's goals (for example from a Poisson distribution with a mean that comes from its
rating), or give each match a win, draw and loss probability. Check your draw rate against
`epl_played.csv`.

## Simplifications you may use

- Break any tie left after points, goal difference and goals scored at random.
- If you simulate results without scores, break ties in points at random.
