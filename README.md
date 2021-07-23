# Chess960
Setup, Nodes after 20 moves, Evaluation

Classical Set up 
```
rnbqkbnr, 1338532, 0.48
```
Best Chess 960 setups
```
nrkbbnrq, 3901301, 0.05
qrnkbnrb, 4097438, 0.07
rnkrbnqb, 4200981, -0.07
qrnknrbb, 4207470, 0.06
bqrbnkrn, 4741986, -0.08
```
How I determined the Best Chess Set Opening? 
The two criteria for an optimal setup: 
1.when the game starts white and black have approximately equal probabilities of winning.
2.There are a maximum of valid many different possible openings. i.e in classical "the sicilian" or "the queen's gambit" exetera

Chess evaluations determine approximately how likely white is to win the game. At the start stockfish evaluates white as 0.48 
which approximately translates to white having a 55% chance of winning (-0.48 would mean black has a 55% chance of winning).
I decided that anything under 0.1 would which give either side a 51% was stasically signifcant enough to warrant being considerend strickly better
than the classical set up. I queried stockfish over the 960 differnet setups using the <<eval>>command. There where approxiametly 
150 setups within the range (-0.1,0.1).
Furthermore to measure the number of possible openings I compared the 150 setups at depth 20 <<go depth 20>>. i,e checking the number of valid possible 
openings after 20 moves of play.There are 1.3 million in the classical setup. In the best setups, I have found some with over 4 million 
which is over 3 times as many as the classical setup.

Sevaral observations on the 5 best Setups
1. Bishops facing the same direction either bb** or b**b occur in all the best setups
2. Kings are already in the corner so castling is more or less optional
3. Queen rook battery is present in 4/5 setups
4. Knights do not seen to follow any opservable patterns

Problems and possible improvements 
1.Stockfish's evaluations at the start are the most unreliable of all their evaluations as there are infinetly many moves that can be played theoretically
versus say an evaulation of a position 20 moves deep. However Since this error is present in all the opening setups we can still evaulate their relative strengths.
Using Leela chess0 evaluations and possibly averaging the two may be a solution.
2. Depth 20 is arbitrary. there is no guarantee However due to the sheer magnitude of difference between 4.7 million and 1.3 million it is clear that bqrbnkrn will be
better than the calssical at any depth greater than 20 due to the law of large numbers. It still may be better to evaluate at depth n n>20 to get a clearer picture of the top 
opening setups
3. I used the number of Nodes which counts bad positions I.e the computer checks e4e5 ke2 desipite being a bad move the computer still checks it and counts it as one of 
the Nodes visited. This means that 4207470 is not necessarily better than 4200981 see above. However when there is a large difference between two setups say 0.5 mill+ we can 
determine 1 to be better than the other.
