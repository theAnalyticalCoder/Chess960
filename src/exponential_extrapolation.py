import subprocess
import pickle
import csv
if __name__ == "__main__":

    line_count = 0
    fens = ["\"nbrkbrnq/pppppppp/8/8/8/8/PPPPPPPP/NBRKBRNQ w FCfc - 0 1\"","\"rkqbbnrn/pppppppp/8/8/8/8/PPPPPPPP/RKQBBNRN w GAga - 0 1\"","\"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w HAha - 0 1\""]
    d_fen_nodes={"nbrkbrnq": [], "rkqbbnrn":[], "rnbqkbnr": []}
    for fen in fens:

        id_fen = fen[1:9]
        for depth in range(20,31):
            s = "setoption name UCI_Chess960 value true\nposition fen " + fen + "\ngo depth "+str(depth)+" \ngo movetime 30000000000000000"
            output = subprocess.run("stockfish", shell=True, capture_output=True, input=s, text=True)

            nodes = 0
            for line in output.stdout.split("\n"):
                words = line.split(" ")
                if "bestmove" == words[0]:
                    nodes = int(prev[11])
                    break
                prev = words
            print(id_fen+" "+ str(depth)+" "+str(nodes))
            d_fen_nodes[id_fen].append(nodes)
    with open('Chess960_nodes.csv', mode='w') as chess:
        chess_writer = csv.writer(chess, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key, val in d_fen_nodes.items():
            chess_writer.writerow([key]+val)
    a_file = open("Chess960_20_to_30.pkl", "wb")
    pickle.dump(d_fen_nodes, a_file)
    a_file.close()