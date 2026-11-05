# NHL 2026-27: playoff format

Snapshot taken Wednesday, November 4, 2026, from the NHL's public API (`api-web.nhle.com`),
regular season only. `nhl_played.csv` has the 246 games played through Tuesday, November 3.
`nhl_remaining.csv` has the other 1,098. Every team plays 84 games this season. `neutral` is
1 for games played away from both teams' arenas.

## Scores, overtime and points

There are no ties. A game tied after regulation goes to overtime, then a shootout. The final
score in the files includes the deciding goal, so the winner always has more goals.

`ot` is 1 when the game was decided in overtime or a shootout, 0 in regulation (blank for
games not yet played). It matters because of how points work:

- A win is 2 points, in regulation, overtime or a shootout.
- A loss in overtime or a shootout is 1 point (the "loser point").
- A loss in regulation is 0 points.

Your simulation has to decide two things for each remaining game: who wins, and whether it
went past regulation. Check how often games went to overtime in `nhl_played.csv` and use
that rate.

## Who makes the playoffs

Eight teams from each conference (Eastern and Western), 16 in all, ranked by points.

- The top three teams in each division make it. There are four divisions: Atlantic and
  Metropolitan in the East, Central and Pacific in the West.
- The two best remaining teams in each conference, from either division, are the wild cards.

## The playoffs

- In each conference, the division winner with more points plays the second wild card, and
  the other division winner plays the first wild card. The 2 and 3 teams in each division
  play each other.
- The bracket is fixed. Every round is best of seven, with home ice to the team with more
  points (games 1, 2, 5 and 7 at home).
- Playoff games are never decided by a shootout, so every playoff game in your simulation
  needs a winner.
- The two conference winners meet in the Stanley Cup Final.

## Simplifications you may use

- Break ties in points with regulation wins (games won with `ot` = 0), then at random.
- Use the same win probability model in the playoffs as in the regular season.
