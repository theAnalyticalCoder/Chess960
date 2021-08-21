
# Chess960
How I determined the Best Chess Setup?   
There are two criteria for an optimal setup:   
1.When the game starts white and black have approximately equal probabilities of winning (50%).  
2.There is a maximum of valid possible openings. i.e in classical "the sicilian" or "the queen's gambit" etc    

  **Setup, Nodes after 30 moves, Evaluation**

**Classical Set up** 
```
rnbqkbnr, 52.9 Million, 0.48
```
**Best Chess 960 setups**
```
rkqbbnrn, 194.2 Million, 0.02
bbnqnrkr, 167.3 Million, 0.13
rbkqbrnn, 166.7 Million, 0.13
nbnrbqkr, 160.3 Million, -0.17
bnrbqkrn, 158.7 Million, -0.13
```


Chess evaluations determine approximately how likely white is to win the game. At the start stockfish evaluates white as 0.48 
which approximately translates to white having a 57% chance of winning (-0.48 would mean black has a 57% chance of winning).

I decided that anything within the range (-0.18,0.18) which give either side a 52.5% of winning was stasically signifcant enough to warrant being considerend strickly better
than the classical set up. I queried stockfish over the 960 differnet setups using the "eval" command. There are
292 setups within the range (-0.18,0.18). 
    
Furthermore to measure the number of possible openings I compared the 200 setups at depth 30 "go depth 30". i,e checking the number of valid possible 
openings after 30 moves of play.There are 52.9 million in the classical setup. In the best setups, I have found some with over 160 million 
which is over 3 times as many as the classical setup.     
    
A Node represents a position, for example playing e4 from the classical setup is a Node so there are fewer than 52.9 million games approximately (35-40%) so 19 million actual games are possible at 30 moves. However, since this will be a fixed percentage common to every setup (i.e no matter what moves you play you have to play 24 moves to get to a game of 25 moves) we can stilluse the number of nodes as a measure of the number of possible openings. I got the 35-40% number as most of these setups follow expontential distributions with base [1.35,1.50].  

The data for all is in 960 Chess960_eval_25_20_fen.pkl it took 12 hr to create. The data only for those setups whose evaluation was in (-0.18,0.18) is in Chess_960_30.pkl which took 12hr to compile despite only containing 292 entries. At depth 35, 1 opening takes 10-20 min so it would take 2-4 days to complete I have it running on an old computer. 40+moves onward could take as long as an hour each opening. Maybe if this gains some traction. We can split up the work accross different computers.

So Is 'rnbqkbnr' the confirmed Best Opening? Sadly No.
 
Lets look at the same Problem but instead only looking at a depth of 25 moves  
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
Notice Anything?
First it took 25 moves for 9.2 Million moves to be reached but only 5 moves (26-30) for 40 million new moves to be recorded. The Horrors of Exponential growth.  
Second Only one of the top 5 at depth 25 is in the Top 5 at depth 30 "rkqbbnrn". So does that mean this is all worthless? Will None of the Top 5 at 25 be in the Top 5 at 30. Yes and No.  
  It becomes necessary to create an approximate distribution for each setup for example an approximate formula for the classical setup is 3338*1.37^x and for rkqbbnrn 
1166*1.5^x where x is the number of moves. I querried stockfish for the number of nodes from 20-30 to construct this distribution i.e doing "go depth 20", "go depth 21"...
    
  We are going to ignore the constant infront and focus only on the bases, 1.37 and 1.5. We need to construct 95% confidence interval for the clasical setup we have the true base is an element of [1.333,1.415] and for rkqbbnrn [1.437,1.556] notice 1.415<1.437 this means we can definitely say (with 95% confidence) that rkqbbnrn is strickly better than the classical setup. 
 ![alt text](https://github.com/theAnalyticalCoder/Chess960/blob/main/Trends.png) 
 
  Looking at the graph it is abundantly clear there is no way the classical setup can ever catch rkqbbnrn. However the approximate setup nbrkbrnq (1st place at 25 moves 25th after 30)has a formula of 3178*1.43^x CI=[1.370,1.492] which means there is some potential overlapwith [1.333,1.415]. As we increase depth we will be able to shrink our confidence intervals and most likely determine 25-50 setups that are optimal. I did not include moves 1-19 since we are only concerned with what happens on the larger scale of the spectrum and these moves would shrink the confidence interval perhaps prematurely.
  
  Todo  
  I will redo this expirement considering only the 292 setups that have an evaluation within (-0.18,0.18) at 35 moves. It will take days... 
    
  Problems and possible improvements   
  1.Stockfish's evaluations at the start are the most unreliable of all their evaluations as there are infinetly many moves that can be played theoretically
versus say an evaulation of a position 20 moves deep. However Since this error is present in all the opening setups we can still evaulate their relative strengths.
Using Leela chess0 evaluations and possibly averaging the two may be a solution.  
  2. I used the number of Nodes which counts bad positions I.e the computer checks e4e5 ke2 desipite being a bad move the computer still checks it and counts it as one of 
the Nodes visited. However once again this is repeated in every evaluation we can expect an approximate percentage 75-80% of the actual number to be correct games. Furthermore 
it under counts some possible games i.e a computer would never play a gambit(giving a pawn for positional advantage) but a human might. These two kind of cancel  so the nodes is still a pretty accurate representation of the number of games possible at x moves 
