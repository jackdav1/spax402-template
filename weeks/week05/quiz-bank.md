# Week 5 quiz bank (core questions)

<!-- /quiz-me asks these plus one dynamic question generated from your own work.
     No answer key lives in this repo — understanding is the answer key. -->

1. A regression on 2,174 team-games says each additional rush attempt is worth +0.94 points of
   final margin, at p < 0.0001. Explain why that number is close to worthless as advice to a
   coach, without using the word "causation."

2. Adding score state drops the rush coefficient from +0.94 to +0.14, and it stays significant at
   p = 6e-9. A teammate reads that as "so running still helps, just less than we thought." Say what
   is incomplete about that reading.

3. Run share by game state goes from 0.32 when a team is down 9+ to 0.55 when it is up 9+. Explain
   how that one table accounts for the collapse of the coefficient in question 2.

4. This analysis uses 2,174 team-games rather than 32 team-seasons, from identical source data.
   Name what specifically goes wrong at n = 32, and why adding predictors makes it worse.

5. Your agent offers to "be thorough" by adding twelve more control variables. Give the reason to
   decline, then name the one control you would add instead and say what question it would settle.
