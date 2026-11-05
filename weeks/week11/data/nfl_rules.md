# NFL 2026: playoff format

Snapshot taken Wednesday, November 4, 2026, from nflverse (`games.csv`, regular season only).
`nfl_played.csv` has the 121 games played through Monday, November 2. `nfl_remaining.csv`
has the other 151. Every team plays 17 games. Teams are nflverse abbreviations (`LA` is the
Rams, `LAC` the Chargers). `neutral` is 1 for games at a neutral site, such as the
international games, where neither team gets home advantage.

## Who makes the playoffs

Seven teams from each conference (AFC and NFC) make the playoffs, 14 in all.

- The four division winners are seeds 1 to 4, ordered by record.
- The three best records among the other teams in the conference are seeds 5 to 7.
- A tie counts as half a win and half a loss.

## The playoff games

- The 1 seed gets a bye. In the wild card round, 2 hosts 7, 3 hosts 6 and 4 hosts 5.
- After each round the bracket is reseeded: the 1 seed hosts the lowest seed left, and the
  other two teams play, with the higher seed at home.
- The two conference winners meet in the Super Bowl at a neutral site.
- Every playoff game is a single game. There are no ties in the playoffs, so your simulation
  needs a winner every time.

## Simplifications you may use

- Break any tie in record (for a division title or a seed) at random. The real tiebreakers
  start with head-to-head and division record; use them if you want to, but you don't have
  to.
- Use the same home advantage in the playoffs as in the regular season, and none in the
  Super Bowl.
