import subprocess
import pickle
if __name__== "__main__":
    '''
    The main idea of this program is to capture three key facts: 
    1.the evaluation at the start of the game
    2.the number of Nodes after 20 moves
    3.the number of Nodes after 25 moves
    
    Each Node represents a position for example from the normal starting position "rnbqkbnr" playing e4 would be a new Node
    (3) will be used as a metric to determine how many games are possible after 25 moves
    (2) and (3) will be used to give an approximate exponential distribution for each set
    the limitations of this approach will be discussed at the bottom of the program not to spoil the fun
    However e4e5 Ke2 would also be a node that could 
    '''
    line_count=0
    eval_nodes_fen=[]
    '''
    Note I did this first with a text file I got from the internet called Chess960.txt with all 960 positions
    or so I thought
    This is what I got [FEN "bbqnnrkr/pppppppp/8/8/8/8/PPPPPPPP/BBQNNRKR w - - 0 1"]
    This is the correct[FEN "bbqnnrkr/pppppppp/8/8/8/8/PPPPPPPP/BBQNNRKR w HFhf - 0 1"]
    Spot the difference?
    HFhf->represents castling privileges I had originally assumed that at move 0 it would be assumed both
    sides could castle but no you need to specify this...
    '''
    with open("Chess960_Correct.txt", "r", encoding="utf-8") as chess:
        for row in chess:
            if line_count == 0:
                line_count += 1
                continue
            print("Line "+str(line_count))
            line_count+=1
            start_index = row.find("[") + 4
            end_index = row.find("]")
            fen=row[start_index:end_index]
            id_fen = fen[2:10]
            '''
            (1):
                set the chess engine to play chess960
                set the position with position fen "+fen+"
                capture the evaluation with eval
            '''
            s="setoption name UCI_Chess960 value true\nposition fen "+fen+"\neval"
            evaluation = subprocess.run("stockfish", shell=True, capture_output=True, input=s, text=True)
            evaluation_per_id=""
            for line in evaluation.stdout.split("\n"):
                words=line.split(" ")
                if "Final" == words[0]:
                    evaluation_per_id = float(words[6])
                    break
            '''
             (2):
                set the chess engine to play chess960
                set the position with position fen "+fen+"
                capture the evaluation after 20 with go depth 20
                there is a bug in the stockfish that if two commands 1 that is short one that is long 
                ex eval\n go depth 20 it will go the first one correctly but abort the second longer one without
                doing it correctly
                So A second useless command go movetime 30000000000000 is used (in theory the correct command would be go infinite but this works)
                if you dont believe me try "setoption name UCI_Chess960 value true\nposition fen "+fen+"\ngo depth 20"
                you'll get the wrong answer
            '''
            s = "setoption name UCI_Chess960 value true\nposition fen "+fen+"\ngo depth 20\ngo movetime 30000000000000"
            depth_20=subprocess.run("stockfish", shell=True, capture_output=True, input=s, text=True)

            nodes_20=0
            for line in depth_20.stdout.split("\n"):
                words=line.split(" ")
                if "bestmove" == words[0]:
                    nodes_20 = int(prev[11])
                    break
                prev=words
            print(nodes_20)
            '''
            (3):
                similar to above with command go depth 25 instead of go depth 20
                why not do this in one function call, Mr. Analyst if you even have any form of Accreditation from Analyst school? 
                   you're right: eval\ngo depth 20\ngo movetime 30000000000000" would be fine 
                   however: go depth 20\ngo depth 25\ngo movetime 30000000000000" would actually give you an incorrect number of nodes for
                   depth 25, stockfish memomized positions so we would get a lower number of actual nodes in depth 25 
            '''
            s = "setoption name UCI_Chess960 value true\nposition fen " + fen + "\ngo depth 25\ngo movetime 30000000000000"
            depth_25 = subprocess.run("stockfish", shell=True, capture_output=True, input=s, text=True)

            nodes_25 = 0
            for line in depth_25.stdout.split("\n"):
                words = line.split(" ")
                if "bestmove" == words[0]:
                    nodes_25 = int(prev[11])
                    break
                prev = words
            print(nodes_25)
            eval_nodes_fen.append((evaluation_per_id,nodes_25,nodes_20,id_fen))
    a_file = open("Chess960_eval_20_25_fen.pkl", "wb")
    pickle.dump(eval_nodes_fen, a_file)
    a_file.close()

   
