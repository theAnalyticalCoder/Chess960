
# Chess960
How I determined the Best Chess Setup?   
The two criteria for an optimal setup:   
1.When the game starts white and black have approximately equal probabilities of winning (50%).  
2.There are a maximum of valid many different possible openings. i.e in classical "the sicilian" or "the queen's gambit" exetera   

  **Setup, Nodes after 25 moves, Evaluation**

**Classical Set up** 
```
rnbqkbnr, 9.2 Million, 0.48
```
**Best Chess 960 setups**
```
nbrkbrnq, 33.3 Million, 0.01
rkqbbnrn, 31.3 Million, 0.02
qrkrnbbn, 29.7 Million, 0.01
rknbbnrq, 29.6 Million, -0.08
brqknbnr, 26.9 Million, -0.02
```


Chess evaluations determine approximately how likely white is to win the game. At the start stockfish evaluates white as 0.48 
which approximately translates to white having a 57% chance of winning (-0.48 would mean black has a 57% chance of winning).

I decided that anything within the range (-0.18,0.18) which give either side a 52.5% of winning was stasically signifcant enough to warrant being considerend strickly better
than the classical set up. I queried stockfish over the 960 differnet setups using the <<eval>>command. There where approxiametly 
200 setups within the range (-0.18,0.18). The data is in Chess960_eval_20_25_fen.pkl.
    
Furthermore to measure the number of possible openings I compared the 200 setups at depth 25 <<go depth 25>>. i,e checking the number of valid possible 
openings after 25 moves of play.There are 9.3 million in the classical setup. In the best setups, I have found some with over 30 million 
which is over 3 times as many as the classical setup.     
    
A Node represents a position, for example playing e4 from the classical setup is a Node so there are approximately 2-4 million games after 25 moves instead of 9.3 million.
However, since this will be a fixed percentage common to every setup (i.e no matter what moves you play you have to play 24 moves to get to a game of 25 moves) we can still
use the number of nodes as a measure of the number of possible openings.

So Is 'nbrkbrnq' the confirmed Best Opening? Sadly No.
 
Lets look at the same Problem but instead only looking at a depth of 20 moves  
**Setup, Nodes after 20 moves, Evaluation**
 **Classical Set up** 
```
rnbqkbnr, 1.50 Million, 0.48
```
**Best Chess 960 setups**
```
rbbnkqrn, 4.56 Million, -0.11
bnnbqrkr, 4.49 Million, 0.08
rkbnnbrq, 4.39 Million, -0.14
nrbknqrb, 4.03 Million, 0.05
qrkbnnbr, 4.02 Million, 0.06
```
Notice Anything?
First it took 20 moves for 4.5 Million moves to be reached but only 5 moves (21-25) for 25 million new moves to be recorded. The Horror of Exponential growth.  
Second None of the Top 5 at depth 20 are in the Top 5 at depth 25. So does that mean this is all worthless? Will None of the Top 5 at 25 be in the Top 5 at 30. Yes and No.  
  It becomes necessary to create an approximate distribution for each setup for example an approximate formula for the classical setup is 3338*1.37^x and for rkqbbnrn 
1166*1.5^x where x is the number of moves.    
    
  We are going to ignore the constant infront and focus only on the bases, 1.37 and 1.5. Using 0.05 to construct 95% confidence interval for the clasical setup we have the true is an element of [1.32,1.42] and for rkqbbnrn [1.45,1.55] notice 1.42<1.45 this means we can definately say (with 95% confidence) that rkqbbnrn is strickly better than the classical setup in fact after 30 moves the classical reaches 52 million Nodes and rkqbbnrn reaches 160 million. It is abundantly clear there is no way the classical setup can ever catch rkqbbnrn. However the approximate setup nbrkbrnq has a formula of 3178*1.43^x CI=[1.38,1.48] which means there is some potential overlap. As we increase depth we will be able to shrink our confidence intervals and most likely determine 25-100 setups that are optimal.
  
  Todo  
  I will redo this expirement considering only the 300 setups that have an evaluation within (-0.18,0.18) at 30 moves. It took 12hrs for 960 at 25 and under an hour for 960 at 20. 30 moves may take 3-4 times as long...    
For the Top 25-50 at 300 moves I will also get the points from 20-30 i.e doing <<go depth 20>> to get a sample set of 10 in which to decrease the confidence interval size.  
    
  Problems and possible improvements   
  1.Stockfish's evaluations at the start are the most unreliable of all their evaluations as there are infinetly many moves that can be played theoretically
versus say an evaulation of a position 20 moves deep. However Since this error is present in all the opening setups we can still evaulate their relative strengths.
Using Leela chess0 evaluations and possibly averaging the two may be a solution.  
  2. I used the number of Nodes which counts bad positions I.e the computer checks e4e5 ke2 desipite being a bad move the computer still checks it and counts it as one of 
the Nodes visited. However once again this is repeated in every evaluation we can expect an approximate percentage 75-80% of the actual number to be correct games. Furthermore 
it under counts some possible games i.e a computer would never play a gambit(giving a pawn for positional advantage) but a human might so the nodes is still a pretty accurate representation of the number of games possible at x moves 
