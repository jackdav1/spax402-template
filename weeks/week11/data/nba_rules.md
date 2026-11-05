# NBA 2026-27: playoff format

Snapshot taken Wednesday, November 4, 2026, from ESPN's public NBA scoreboard (regular season
only). `nba_played.csv` has the 107 games played through Monday, November 2.
`nba_remaining.csv` has the other 1,093 games that are on the schedule. `neutral` is 1 for
the three games played away from both teams' arenas, where neither team gets home advantage.

## The two missing games per team

Each team plays 82 games, but only 80 per team are in these files. The last two are set in
December after the NBA Cup group stage: Cup quarterfinal and semifinal games count in the
standings, and teams knocked out of the Cup get extra games instead. Those games don't have
opponents yet, so they aren't in `nba_remaining.csv`.

You may either simulate the 80 games you have, or add two games for every team against
random opponents from its own conference. Say which one you did.

## Who makes the playoffs

Fifteen teams in each conference (East and West), ordered by record.

- Seeds 1 to 6 go straight into the playoffs.
- Seeds 7 to 10 play in the play-in tournament:
  - 7 hosts 8. The winner is the 7 seed.
  - 9 hosts 10. The loser is out.
  - The loser of 7 against 8 hosts the winner of 9 against 10. The winner is the 8 seed.

## The playoffs

- Sixteen teams, eight in each conference. In each conference, 1 plays 8, 4 plays 5, 3
  plays 6 and 2 plays 7, and the bracket is fixed (no reseeding).
- Every round is best of seven. The team with the better record has home court: games 1, 2,
  5 and 7 at home.
- The two conference champions meet in the NBA Finals, also best of seven, with home court
  to the better record.

## Simplifications you may use

- Break any tie in record at random.
- You can simulate a best-of-seven series game by game, or from a single series win
  probability. Game by game is easier to get right.
