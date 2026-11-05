# College football 2026: conference title games

Snapshot taken Wednesday, November 4, 2026, from ESPN's public scoreboard (FBS, regular
season). Team names are ESPN's full names, such as "Delaware Blue Hens".

- `cfb_played.csv` has the 624 games played through Tuesday, November 3 that involved an FBS
  team. That includes 122 games against FCS teams, marked `fcs_opponent` = 1. FCS teams show
  up with conference "FCS".
- `cfb_remaining.csv` has the 259 games left that are FBS against FBS.
- Nine games are in neither file. Wake Forest, Ole Miss, Mississippi State, Alabama and
  Auburn each have one game left against an FCS team. Colorado State, Fresno State, Utah
  State and Washington State each play a Pac-12 game on December 5 against an opponent the
  standings decide. None of the nine affects who reaches a title game.
- The conference championship games are not in either file. Those are what you simulate.
- `conf_game` is 1 for games that count in the conference standings. `neutral` is 1 for
  neutral-site games.

## What gets simulated

Which two teams reach each conference's title game, and who wins it. The Sun Belt has two
divisions (East and West, shown in `home_conf` and `away_conf`), and its title game is the
East winner against the West winner. Every other conference with a title game sends the two
teams with the best conference record: the American, ACC, Big 12, Big Ten, Conference USA,
MAC, Mountain West, Pac-12 and SEC.

FBS Independents, such as Notre Dame, have no title game.

## Simplifications you may use

- Rank teams by conference winning percentage, from games with `conf_game` = 1.
- Break ties with head-to-head when two tied teams played each other, otherwise at random.
  The real tiebreakers go much deeper (records against common opponents, computer rankings
  and more), and you don't need them.
- Play the title game at a neutral site.
- If you want a stretch, simulate the 12-team College Football Playoff too. You will need a
  rule for the committee's ranking, and that rule is the hard part.
