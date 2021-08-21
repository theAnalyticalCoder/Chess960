
# Chess960
How I determined the Best Chess Setup?   
There are two criteria for an optimal setup:   
1.When the game starts white and black have approximately equal probabilities of winning (50%).  
2.There is a maximum of valid possible openings. i.e in classical "the sicilian" or "the queen's gambit" etc    

  **Setup, Games after 30 moves, % White wins**

**Classical Set up** 
```
rnbqkbnr, 15.9 Million, 56%
```
**Best Chess 960 setups**
```
rkqbbnrn, 52.3 Million, 50.2%
bbnqnrkr, 50.2 Million, 51.9%
rbkqbrnn, 50.0 Million, 51.9%
nbnrbqkr, 48.1 Million, 47.6%
bnrbqkrn, 47.6 Million, 48.1%
```


Chess evaluations determine approximately how likely white is to win the game. At the start stockfish evaluates white as 0.48 using the formula from [this site](https://www.chessprogramming.org/Pawn_Advantage,_Win_Percentage,_and_Elo)
which approximately translates to white having a 56% chance of winning (-0.48 would mean black has a 56% chance of winning). This formula slightly overestimates whites chances of winning by 0.8% vs empirical data.

I decided that anything within the range (-0.18,0.18) which give either side a max 52.5% of winning was stasically signifcant enough to warrant being considerend strickly better
than the classical set up. I queried stockfish over the 960 differnet setups using the "eval" command. There are
292 setups within the range (-0.18,0.18). 
    
Furthermore to measure the number of possible openings I compared the 200 setups at depth 30 "go depth 30". i,e checking the number of valid possible 
openings after 30 moves of play.There are 15.9 million in the classical setup. In the best setups, I have found some with over 50 million 
which is over 3 times as many as the classical setup.     
    
Note stockfish outputs Nodes not games. A Node represents a position, for example playing e4 from the classical setup is a Node. So there are many more nodes than actual games. There are in fact 52.9 Million Nodes for the classical setup and 197 Million for rkqbbnrn. If you want to get to game of 30 moves you have to play a game of 29 moves. So 197 mill represents the sum of all the games of 1 move, 2 moves, ... 30 moves. but we only care about the games of 30 moves. To get the number of games I multiplied the number of nodes by 30% because each of the distribution are expontial with a base in [1.35,1,45] to be exact you would be to find the base for the distribution then calculate what the percentage of new nodes is i.e [27%,32%]. This would only increase the discrepency between rkqbbnrn and rnbqkbnr. 

The data for all is in 960 Chess960_eval_25_20_fen.pkl. This is the number of nodes not games to get the number of games multiply by 0.3 and the evaluations need to be changed into percentage using the formula above. It took 12 hr to create. The data only for those setups whose evaluation was in (-0.18,0.18) is in Chess_960_30.pkl which took 12hr to compile despite only containing 292 entries. At depth 35, 1 opening takes 10-20 min so it would take 2-4 days to complete. 40+moves onward could take as long as an hour each opening. Maybe if this gains some traction. We can split up the work accross different computers.

So Is 'rnbqkbnr' the confirmed Best Opening? Sadly No.
 
Lets look at the same Problem but instead only looking at a depth of 25 moves  
  **Setup, Games after 25 moves, % White wins**

**Classical Set up** 
```
rnbqkbnr, 2.8 Million, 56%
```
**Best Chess 960 setups**
```
nbrkbrnq, 10.0 Million, 50.1%
rkqbbnrn, 9.4 Million, 50.2%
qrkrnbbn, 8.9 Million, 50.1%
rknbbnrq, 8.9 Million, 48.8%
brqknbnr, 8.1 Million, 49.8%
```
Notice Anything?
First it took 25 moves for 2.8 Million games to be reached but only 5 moves (26-30) for 13 million new moves to be recorded. The Horrors of Exponential growth.  
Second Only one of the top 5 at depth 25 is in the Top 5 at depth 30 "rkqbbnrn". So does that mean this is all worthless? Will None of the Top 5 at 25 be in the Top 5 at 30. Yes and No.  
  It becomes necessary to create an approximate distribution for each setup for example an approximate formula for the classical setup is 1232*1.362^x and for rkqbbnrn 
1146*1.423^x where x is the number of moves. I querried stockfish for the number of nodes from 20-35 to construct this distribution i.e doing "go depth 20", "go depth 21"...
    
  We are going to ignore the constant infront and focus only on the bases, 1.362 and 1.461. We need to construct 95% confidence interval for the clasical setup we have the true base is an element of [1.340,1.384] and for rkqbbnrn [1.385,1.461] notice 1.384<1.385 this means we can definitely say (with 95% confidence) that rkqbbnrn is strickly better than the classical setup but its close. 
 ![alt text](https://github.com/theAnalyticalCoder/Chess960/blob/main/Trend_new.png) 
 
  Looking at the graph it is abundantly clear there is no way the classical setup can ever catch rkqbbnrn. As we increase depth we will be able to shrink our confidence intervals and most likely determine 25-50 setups that are optimal. As of right now we can realistically only say the top five we are 95% sure are better than the classical setup. I did not include moves 1-19 since we are only concerned with what happens on the larger scale of the spectrum and these moves would shrink the confidence interval perhaps prematurely.
  
  Todo  
  I will redo this expirement considering only the 292 setups that have an evaluation within (-0.18,0.18) at 35 moves. It will take days... 
    
  Problems and possible improvements   
  1.Stockfish's evaluations at the start are the most unreliable of all their evaluations as there are infinetly many moves that can be played theoretically
versus say an evaulation of a position 20 moves deep. However Since this error is present in all the opening setups we can still evaulate their relative strengths.
Using Leela chess0 evaluations and possibly averaging the two may be a solution.  
  2. I used the number of Nodes which counts bad positions I.e the computer checks e4e5 ke2 desipite being a bad move the computer still checks it and counts it as one of 
the Nodes visited. However once again this is repeated in every evaluation we can expect an approximate percentage 75-80% of the actual number to be correct games. Furthermore 
it under counts some possible games i.e a computer would never play a gambit(giving a pawn for positional advantage) but a human might. These two kind of cancel  so the nodes is still a pretty accurate representation of the number of games possible at x moves 
